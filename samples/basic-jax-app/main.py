import asyncio
from storm.common import Get, Module, Controller, Logger, Injectable, Sse
from storm.core import StormApplication
import jax
import jax.numpy as jnp
from jax import random


# JAX-optimized functions
@jax.jit
def lj_jax_array(r):
    sr6 = (1.0 / r) ** 6
    pot = 4.0 * (sr6 * sr6 - sr6)
    return pot


@jax.jit
def distances_jax_array(cluster):
    diff = cluster[:, None, :] - cluster[None, :, :]
    mat = jnp.sum(diff**2, axis=-1)
    return jnp.sqrt(mat)


@jax.jit
def potential_jax_array(cluster):
    d = distances_jax_array(cluster)
    d = jnp.triu(d)  # Zero out lower triangle
    energy = jnp.sum(jnp.where(d > 1e-6, lj_jax_array(d), 0.0))
    return energy

@Injectable()
class JaxService:
    def __init__(self):
        # Warm up the JAX functions with dummy data during initialization
        dummy_cluster = jnp.array(jax.random.uniform(jax.random.PRNGKey(0), (10, 3)))
        potential_jax_array(dummy_cluster)

    @staticmethod
    def compute_potential(cluster):
        return potential_jax_array(cluster)

    async def stream(self, random_key):

        for _ in range(10):
            # Generate the cluster once at the beginning
            random_key, subkey = random.split(random_key)
            cluster = jnp.array(jax.random.uniform(subkey, (100, 50)))
            energy = self.compute_potential(cluster).item()
            yield {"data": {"cluster": cluster, "energy": energy}}
            await asyncio.sleep(0.1)  # Simulate some delay

        yield {"data": {"done": True}}

@Controller()
class ProcessController:
    jax_service: JaxService

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.random_key = random.PRNGKey(0)

    @Get("process")
    async def process(self):
        self.random_key, subkey = random.split(self.random_key)
        cluster = jnp.array(jax.random.uniform(subkey, (1000, 50)))
        return {
            "e": self.jax_service.compute_potential(cluster).item(),
            "cluster": cluster.tolist(),
        }

    @Sse("stream")
    async def stream(self):
        return self.jax_service.stream(self.random_key)


@Module(controllers=[ProcessController], imports=[], providers=[JaxService])
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
