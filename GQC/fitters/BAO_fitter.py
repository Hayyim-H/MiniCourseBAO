# BAO fitter using Y3 unblinded with Neff for Xi
# Basic
import numpy as np
import matplotlib.pyplot as plt
import time
# desilike stuff
from cosmoprimo import fiducial
from desilike.theories.galaxy_clustering import BAOPowerSpectrumTemplate, DampedBAOWigglesTracerCorrelationFunctionMultipoles
from desilike.observables.galaxy_clustering import TracerCorrelationFunctionMultipolesObservable, BoxFootprint, ObservablesCovarianceMatrix
from desilike.likelihoods import ObservablesGaussianLikelihood
from desilike.profilers import MinuitProfiler
from desilike.samplers import EmceeSampler
from desilike.samples import plotting

start = time.time_ns()

basepath = '/path/to/BAO/'

# Cosmology
cosmo_temp = fiducial.AbacusSummit(name='000', engine='class')
# Redshift
zeff = 0.8
# Smoothing scale
smoothing_radius = 10
# Cut scale
smin = 50.
smax = 150.
ds = 4.

# Parameters
apmode = 'qparqper'
rec_mode = 'recsym'
broadband = 'power3'
# outdir = args.outdir

# Derived parameters
ells = (0,) if apmode == 'qiso' else (0, 2)
slim = {ell: [smin, smax, ds] for ell in ells}

# Data
poles = np.loadtxt(basepath + "data/data.txt")
s_arr = poles[:, 0]
nbins = s_arr.shape[0]
data = np.concatenate([poles[:, 1], poles[:, 2]])
# Covariance
cov = np.loadtxt(basepath + "data/cov.txt")

# Template
template = BAOPowerSpectrumTemplate(
                                    z=zeff, 
                                    fiducial=cosmo_temp, 
                                    apmode=apmode, 
                                    with_now='wallish2018',
                                   )
# Theory
theory = DampedBAOWigglesTracerCorrelationFunctionMultipoles(
                                                             template=template, 
                                                             mode=rec_mode,
                                                             smoothing_radius=smoothing_radius,
                                                             broadband=broadband,
                                                            )
# Sigmas (no free-damping)
for param in theory.params.select(basename='sigma*'):
        param.update(fixed=False)
# Observable
observable = TracerCorrelationFunctionMultipolesObservable(
                                                           data=data, 
                                                           covariance=cov,
                                                           theory=theory, 
                                                           ells=ells,
                                                           slim=slim,
                                                           s=s_arr,
                                                          )
# Likelihood
likelihood = ObservablesGaussianLikelihood(observables=[observable])
# Fix some parameters
for param in likelihood.all_params.select(basename=['al4_*', 'bl4_*']):
    param.update(fixed=True)
# Priors
if rec_mode:
    sigmas = 2.0; sigmapar = 6.0; sigmaper = 3.0
else:
    sigmas = 2.0; sigmapar = 9.0; sigmaper = 4.5
likelihood.all_params['sigmas'].update(fixed=False, prior={'dist':'norm','loc': sigmas, 'scale': 2., 'limits': [0., 20]})
likelihood.all_params['sigmapar'].update(fixed=False, prior={'dist':'norm','loc': sigmapar, 'scale': 2., 'limits': [0., 20]})
likelihood.all_params['sigmaper'].update(fixed=False, prior={'dist':'norm','loc': sigmaper, 'scale': 1., 'limits': [0., 20]})

profiler = MinuitProfiler(likelihood, seed=42)
profiles = profiler.maximize(niterations=10)
likelihood(**profiles.bestfit.choice(input=True))

print(profiles.to_stats(tablefmt='pretty'))

chains = 4
sampler = EmceeSampler(likelihood, chains=chains, nwalkers=40, seed=42)
sampler.run(min_iterations=200, max_iterations=1000, check={'max_eigen_gr': 0.03})
chain = sampler.chains[0].remove_burnin(0.5)[::10]

print(chain.to_stats(tablefmt='pretty'))