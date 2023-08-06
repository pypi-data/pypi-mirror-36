from __future__ import division
import sys
import os
import numpy as np
from math import log
from collections import deque
from random import random,randrange
import signal

from . import parameter
from .proposal import DefaultProposalCycle
from . import proposal
from .cpnest import CheckPoint, RunManager

import pickle
__checkpoint_flag = False


class Sampler(object):
    """
    Sampler class.
    Initialisation arguments:
    
    usermodel:
    user defined model to sample
    
    maxmcmc:
    maximum number of mcmc steps to be used in the sampler
    
    verbose:
    display debug information on screen
    default: False
    
    poolsize:
    number of objects for the affine invariant sampling
    default: 1000
    
    seed:
    Random seed
    
    proposal:
    JumpProposal class to use (defaults to proposals.DefaultProposalCycle)
    
    """

    def __init__(self,
                 usermodel,
                 maxmcmc,
                 seed        = None,
                 output      = None,
                 verbose     = False,
                 poolsize    = 1000,
                 proposal    = None,
                 resume_file = None,
                 manager     = None):

        self.seed = seed
        self.user = usermodel
        self.initial_mcmc = maxmcmc//10
        self.maxmcmc = maxmcmc
        self.resume_file = resume_file
        self.manager = manager
        self.logLmin = self.manager.logLmin
        
        if proposal is None:
            self.proposal = DefaultProposalCycle()
        else:
            self.proposal = proposal

        self.Nmcmc = self.initial_mcmc
        self.Nmcmc_exact = float(self.initial_mcmc)

        self.poolsize = poolsize
        self.evolution_points = deque(maxlen=self.poolsize)
        self.verbose=verbose
        self.sub_acceptance=0.0
        self.mcmc_accepted = 0
        self.mcmc_counter = 0
        self.initialised=False
        self.output = output
        self.samples = [] # the list of samples from the mcmc chain
        self.ACLs = [] # the history of the ACL of the chain, will be used to thin the output, if requested
        self.producer_pipe = self.manager.connect_producer()
        
    def reset(self):
        """
        Initialise the sampler
        """
        np.random.seed(seed=self.seed)
        for n in range(self.poolsize):
            while True: # Generate an in-bounds sample
                if self.verbose > 2: sys.stderr.write("process {0!s} --> generating pool of {1:d} points for evolution --> {2:.0f} % complete\r".format(os.getpid(), self.poolsize, 100.0*float(n+1)/float(self.poolsize)))
                p = self.user.new_point()
                p.logP = self.user.log_prior(p)
                if np.isfinite(p.logP): break
            p.logL=self.user.log_likelihood(p)
            if p.logL is None or not np.isfinite(p.logL):
                print("Warning: received non-finite logL value {0} with parameters {1}".format(str(p.logL), str(p)))
                print("You may want to check your likelihood function to improve sampling")
            self.evolution_points.append(p)

        if self.verbose > 2: sys.stderr.write("\n")

        self.proposal.set_ensemble(self.evolution_points)
        # Now, run evolution so samples are drawn from actual prior
        for k in range(self.poolsize):
            if self.verbose > 1: sys.stderr.write("process {0!s} --> distributing pool of {1:d} points from the prior --> {2:.0f} % complete\r".format(os.getpid(), self.poolsize, 100.0*float(k+1)/float(self.poolsize)))
            _, _, p = next(self.yield_sample(-np.inf))
        
        if self.verbose > 1: sys.stderr.write("\n")
        if self.verbose > 2: sys.stderr.write("Initial estimated ACL = {0:d}\n".format(self.Nmcmc))
        self.proposal.set_ensemble(self.evolution_points)
        self.initialised=True

    def estimate_nmcmc(self, safety=5, tau=None):
        """
        Estimate autocorrelation length of chain using acceptance fraction
        ACL = (2/acc) - 1
        multiplied by a safety margin of 5
        Uses moving average with decay time tau iterations (default: self.poolsize)
        Taken from W. Farr's github.com/farr/Ensemble.jl
        """
        if tau is None: tau = self.maxmcmc/safety#self.poolsize

        if self.sub_acceptance == 0.0:
            self.Nmcmc_exact = (1.0 + 1.0/tau)*self.Nmcmc_exact
        else:
            self.Nmcmc_exact = (1.0 - 1.0/tau)*self.Nmcmc_exact + (safety/tau)*(2.0/self.sub_acceptance - 1.0)
        
        self.Nmcmc_exact = float(min(self.Nmcmc_exact,self.maxmcmc))
        self.Nmcmc = max(safety,int(self.Nmcmc_exact))
#        if self.verbose >=3:
#            if self.counter%(self.poolsize) == 0:
#                if len(self.samples) > 2*self.maxmcmc:
#                    import numpy.lib.recfunctions as rfn
#                    print("computing actual ACF\n")
#                    mcmc_samples = rfn.stack_arrays([self.samples[j].asnparray() for j in range(0,len(self.samples))],usemask=False)
#                    print mcmc_samples.dtype.names
#                    for n in mcmc_samples.dtype.names:
#                        if n!='logL' and n!='logPrior':
#                            print mcmc_samples[n].dtype
#                            acf = 2.0*autocorrelation(mcmc_samples[n]).cumsum()-1.0
#                            print "n",acl(acf),self.Nmcmc
        return self.Nmcmc

    def produce_sample(self):
        try:
            self._produce_sample()
        except CheckPoint:
            self.checkpoint()
    
    def _produce_sample(self):
        """
        main loop that generates samples and puts them in the queue for the nested sampler object
        """
        
        if not self.initialised:
          self.reset()

        self.counter=1
        __checkpoint_flag=False
        while True:
            if self.manager.checkpoint_flag.value:
                self.checkpoint()
                sys.exit()
            
            if self.logLmin.value==np.inf:
                break
            
            p = self.producer_pipe.recv()

            if p is None:
                break
            
            self.evolution_points.append(p)
            (acceptance,Nmcmc,outParam) = next(self.yield_sample(self.logLmin.value))

            # Send the sample to the Nested Sampler
            self.producer_pipe.send((acceptance,Nmcmc,outParam))
            # Update the ensemble every now and again
            if (self.counter%(self.poolsize//10))==0:
                self.proposal.set_ensemble(self.evolution_points)
            self.counter += 1

        sys.stderr.write("Sampler process {0!s}: MCMC samples accumulated = {1:d}\n".format(os.getpid(),len(self.samples)))
        self.samples.extend(self.evolution_points)
        import numpy.lib.recfunctions as rfn
        if self.verbose >=3:
            self.mcmc_samples = rfn.stack_arrays([self.samples[j].asnparray()
                                                  for j in range(0,len(self.samples))],usemask=False)
            np.savetxt(os.path.join(self.output,'mcmc_chain_%s.dat'%os.getpid()),
                       self.mcmc_samples.ravel(),header=' '.join(self.mcmc_samples.dtype.names),
                       newline='\n',delimiter=' ')
            sys.stderr.write("Sampler process {0!s}: saved {1:d} mcmc samples in {2!s}\n".format(os.getpid(),len(self.samples),'mcmc_chain_%s.dat'%os.getpid()))
        sys.stderr.write("Sampler process {0!s} - mean acceptance {1:.3f}: exiting\n".format(os.getpid(), float(self.mcmc_accepted)/float(self.mcmc_counter)))
        return 0

    def checkpoint(self):
        """
        Checkpoint its internal state
        """
        print('Checkpointing Sampler')
        with open(self.resume_file, "wb") as f:
            pickle.dump(self, f)
        sys.exit(0)

    @classmethod
    def resume(cls, resume_file, manager):
        print('Resuming Sampler from '+resume_file)
        with open(resume_file, "rb") as f:
            obj = pickle.load(f)
        obj.manager = manager
        obj.logLmin = obj.manager.logLmin
        obj.producer_pipe = obj.manager.connect_producer()
        return(obj)

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['logLmin']
        del state['manager']
        del state['producer_pipe']
        return state
    
    def __setstate__(self, state):
        self.__dict__ = state
        self.manager = None

class MetropolisHastingsSampler(Sampler):
    def yield_sample(self, logLmin):
        """
        metropolis-hastings loop to generate the new live point taking nmcmc steps
        """
        while True:
            sub_counter = 0
            sub_accepted = 0
            oldparam = self.evolution_points.popleft()
            logp_old = self.user.log_prior(oldparam)

            while True:
                sub_counter += 1
                newparam = self.proposal.get_sample(oldparam.copy())
                newparam.logP = self.user.log_prior(newparam)
                if newparam.logP-logp_old + self.proposal.log_J > log(random()):
                    newparam.logL = self.user.log_likelihood(newparam)
                    if newparam.logL > logLmin:
                        oldparam = newparam
                        logp_old = newparam.logP
                        sub_accepted+=1
                if (sub_counter >= self.Nmcmc and sub_accepted > 0 ) or sub_counter >= self.maxmcmc:
                    break
        
            # Put sample back in the stack, unless that sample led to zero accepted points
            self.evolution_points.append(oldparam)
            if self.verbose >=3:
                self.samples.append(oldparam)
            self.sub_acceptance = float(sub_accepted)/float(sub_counter)
            self.estimate_nmcmc()
            self.mcmc_accepted += sub_accepted
            self.mcmc_counter += sub_counter
            # Yield the new sample
            if oldparam.logL > logLmin:
                yield (float(self.sub_acceptance),sub_counter,oldparam)

class HamiltonianMonteCarloSampler(Sampler):
    def yield_sample(self, logLmin):
        while True:
            sub_accepted = 0
            sub_counter = 0
            while not sub_accepted:
                oldparam = self.evolution_points.popleft()
                newparam = self.proposal.get_sample(oldparam.copy(), logLmin)
                sub_counter += 1
                if self.proposal.log_J > np.log(random()):
                    sub_accepted += 1
                    oldparam = newparam
                self.evolution_points.append(oldparam)
#            print("acc: {0:f} sub counter = {1:d} {2:s} {3:f} {4:f}".format(self.proposal.log_J,
#                                                                              sub_counter,
#                                                                 oldparam,
#                                                                 oldparam.logP,
#                                                                 oldparam.logL))
            self.sub_acceptance = float(sub_accepted)/float(sub_counter)
            self.mcmc_accepted += sub_accepted
            self.mcmc_counter  += sub_counter
            if newparam.logL > logLmin:
                yield (float(self.sub_acceptance),sub_counter,oldparam)

def autocorrelation(x) :
    """
    Compute the autocorrelation of the signal, based on the properties of the
    power spectral density of the signal.
    """
    xp = x-np.mean(x)
    f = np.fft.fft(xp)
    p = np.array([np.real(v)**2+np.imag(v)**2 for v in f])
    pi = np.fft.ifft(p)
    return np.real(pi)[:x.shape[0]//2]/np.sum(xp**2)

def acl(acf):
    for i in range(len(acf)//2):
        if acf[i] < i/5.0:
            return acf[i]
