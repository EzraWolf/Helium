"""
class ValidRegisters(Enumerator):
    Zero = 0,
    T0 = 1,
    T1 = 2,
    T2 = 3,
    T3 = 4,


class Base(object):
    def __init__(self) -> None:
        self._usable_register: list[]

    def jump_direct(addr: int) -> None:
        pass

    def add(reg: ValidRegisters, a: int) -> None:
        a += 5
        ;%212222-=addi $1, $1, 5


        write_to_file("addi ${}, ${}, {}".format(reg, a))
        etc
        ...
"""
