import inspect
import asyncio
import atexit
from pygears.core.err import register_exit_hook
from pygears import registry, GearDone
from pygears.sim import clk, timestep, delta, sim_log, sim_phase
from pygears.sim.sim import cancel
from pygears.typing_common.codec import code
from pygears.typing import typeof, TLM


def is_async_gen(func):
    return bool(func.__code__.co_flags & inspect.CO_ASYNC_GENERATOR)


def is_simgear_func(func):
    return inspect.iscoroutinefunction(func) or is_async_gen(func)


class SimGear:
    def __init__(self, gear):
        self.gear = gear
        self.out_queues = []
        self.namespace = registry('SimMap')
        self.done = False
        self._clean = True
        if not hasattr(self, 'func'):
            self.func = gear.func

    @property
    def sim_func_args(self):
        args = []
        for p in self.gear.in_ports:
            args.append(p.consumer)

        kwds = {
            k: self.gear.params[k]
            for k in self.gear.kwdnames if k in self.gear.params
        }

        return args, kwds

    def finish(self):
        self.done = True
        # self.task.cancel()
        for port in self.gear.out_ports:
            port.producer.finish()

        if not self._clean:
            self.cleanup()

    def cleanup(self):
        self._clean = True

    def setup(self):
        self._clean = False
        atexit.register(self.finish)
        register_exit_hook(self.cleanup)
        if self.gear.params['sim_setup'] is not None:
            self.gear.params['sim_setup'](self.gear)

    async def run(self):
        self.task = asyncio.Task.current_task()
        args, kwds = self.sim_func_args

        # out_ports = self.gear.out_ports
        # if len(out_ports) == 1:
        #     out_ports = out_ports[0]

        out_prods = [p.producer for p in self.gear.out_ports]
        single_output = len(out_prods) == 1
        if single_output:
            out_prods = out_prods[0]

        sim = registry('Simulator')

        try:
            if is_async_gen(self.func):
                while(1):
                    if sim.phase != 'forward':
                        await clk()

                    async for val in self.func(*args, **kwds):
                        if sim.phase != 'forward':
                            await clk()

                        if val is not None:
                            if single_output:
                                out_prods.put_nb(val)
                                await out_prods.ready()
                            else:
                                for p, v in zip(out_prods, val):
                                    if v is not None:
                                        p.put_nb(v)

                                for p, v in zip(out_prods, val):
                                    if v is not None:
                                        await p.ready()

                    if args:
                        if all(a.done() for a in args):
                            raise GearDone
            else:
                while (1):
                    await self.func(*args, **kwds)

                    if args:
                        if all(a.done() for a in args):
                            raise GearDone

        except GearDone as e:
            for p in self.gear.in_ports:
                intf = p.consumer
                if not intf.empty():
                    prod_intf = intf.in_queue.intf
                    prod_gear = prod_intf.consumers[0].gear
                    cancel(prod_gear)

            self.finish()
            raise e
