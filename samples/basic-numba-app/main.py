from storm.common import Get, Module, Controller, Logger, Injectable
from storm.core import StormApplication
import numba
import numpy as np


# Numba-optimized functions
@numba.njit
def lj_numba_array(r):
    sr6 = (1. / r) ** 6
    pot = 4. * (sr6 * sr6 - sr6)
    return pot


@numba.njit
def distances_numba_array(cluster):
    diff = (cluster.reshape(cluster.shape[0], 1, cluster.shape[1]) -
            cluster.reshape(1, cluster.shape[0], cluster.shape[1]))
    mat = (diff * diff)
    out = np.empty(mat.shape[:2], dtype=mat.dtype)
    for i in np.ndindex(out.shape):
        out[i] = mat[i].sum()

    return np.sqrt(out)


@numba.njit
def potential_numba_array(cluster):
    d = distances_numba_array(cluster)
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            if i > j:
                d[i, j] = 0

    energy = 0.0
    for v in d.flat:
        if v > 1e-6:
            energy += lj_numba_array(v)
    return energy


@Injectable()
class NumbaService:

    def __init__(self):
        # Warm up the Numba functions with dummy data during initialization
        dummy_cluster = np.random.rand(10, 3)  # Small test data
        potential_numba_array(dummy_cluster)

    @staticmethod
    def compute_potential(cluster):
        return potential_numba_array(cluster)


@Controller("/process")
class ProcessController:

    numba_service: NumbaService

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @Get()
    async def process(self):
        cluster = np.random.rand(100, 50)
        return {
            "e": self.numba_service.compute_potential(cluster),
        }


@Module(controllers=[ProcessController], imports=[], providers=[NumbaService])
class UsersModule:
    pass


@Module(imports=[UsersModule])
class AppModule:
    pass


# Initialize the application with AppModule
app = StormApplication(AppModule)

if __name__ == "__main__":
    # Start the application
    app.run()
