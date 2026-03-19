from cobaya.likelihood import Likelihood
from cobaya.conventions import Const
import numpy as np

class desi2025_all(Likelihood):
    # Before you define the functions, you can add here global variables.
    # In this case we define the path to the files as a variable that Cobaya can give us.
    data_file: str
    cov_file: str

    def initialize(self):
        # You can import codes o files in here.

        # First we need to read the data.
        z_arr, data_arr, self.dist_type = np.loadtxt(self.data_file, dtype=str, unpack=True)

        self.z = z_arr.astype(float)
        self.data = data_arr.astype(float)

        # Now we read the covariance matrix and invert it.
        self.cov = np.loadtxt(self.cov_file)
        self.inv_cov = np.linalg.inv(self.cov) 


    def get_requirements(self):
        # Here we need to define the parameters or quantities that the theory code can give us.
        # Check the documentation for the must_provide() function in https://cobaya.readthedocs.io/en/latest/ to the complete list of quantities that CLASS and CAMB can clculate and how to invoque them.
        # Specifically, you need to define a python dictionary here. 
        return {
            "comoving_radial_distance": {'z': self.z},
            "Hubble": {'z': self.z},
            "rs_drag": None
        }


    def logp(self, **params_values):
        # As the name says, this function needs to return the log-likelihood value.

        # First we need the different quantities from theory
        rs_theory = self.provider.get_param("rs_drag")
        DM_theory = self.provider.get_comoving_radial_distance(self.z)
        H_theory = self.provider.get_Hubble(self.z)
        # Remember that DH(z) = c/H(z)
        DH_theory = Const.c_km_s/H_theory

        DM_dict = dict(zip(self.z, DM_theory))
        DH_dict = dict(zip(self.z, DH_theory))
        theory = np.zeros_like(self.data)

        for i, (z_val, d_type) in enumerate(zip(self.z, self.dist_type)):

            dm = DM_dict[z_val]
            dh = DH_dict[z_val]

            if d_type == "DM_over_rs":
                theory[i] = dm/rs_theory
            
            elif d_type == "DH_over_rs":
                theory[i] = dh/rs_theory

            elif d_type == "DV_over_rs":
                dv = (z_val * dm**2 * dh)**(1/3)
                theory[i] = dv/rs_theory

            else:
                raise ValueError(f"¡Etiqueta no reconocida en el catálogo!: {d_type}")
            
        # Comparing data vs theory
        delta = self.data - theory

        # Here we calculate the loglike value
        chi2 = np.dot(delta, np.dot(self.inv_cov, delta))
        logLike = -0.5 * chi2

        return logLike