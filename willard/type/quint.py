from willard.const import gate
from willard.type import qbit, qbits


class quint:
    def __init__(self, qr, size: int, offset: int, init_value: int) -> None:
        self.qr = qr
        self.size = size
        self.offset = offset
        b = format(init_value, 'b')
        if len(b) > size:
            raise ValueError("init_value is bigger than the size of qint.")
        b_rev = b[::-1]
        for i, elem in enumerate(b_rev):
            if elem == '1':
                self[i].x()

    def __getitem__(self, idx):
        if type(idx) == int:
            self._check_idx(idx)
            return qbit(self.qr, self.offset + idx)
        elif type(idx) == slice:
            indices = set(range(idx.start, idx.stop, idx.step))
            for i in indices:
                self._check_idx(i)
            indices = set([i + self.offset for i in indices])
            return qbits(self.qr, indices)
        elif type(idx) == tuple or type(idx) == list:
            indices = set()
            for i in idx:
                if type(i) == slice:
                    indices = indices | set(
                        range(idx.start, idx.stop, idx.step))
                    for i_ in indices:
                        self._check_idx(i_)
                elif type(i) == int:
                    self._check_idx(i)
                    indices.add(i)
            indices = set([i + self.offset for i in indices])
            return qbits(self.qr, indices)

    def measure(self):
        result = ''
        for i in range(self.size):
            result = str(self[i].measure()) + result
        return int(result, 2)

    def swap_test(self, *, input1: int, input2: int, output: int):
        """
        0 if input1 != input2
        1 if input1 == input2
        1 or 0 when input1 and input2 resembles
        """
        self.h(output)
        self.cswap(c=output, d1=input1, d2=input2)
        self.h(output)
        self.x(output)
        return self

    def inc(self):
        for i in reversed(range(self.size)):
            cs = []
            for j in reversed(range(i)):
                cs.append(j)
            self[cs].cu(self[i], gate.x)
        return self

    def dec(self):
        for i in range(self.size):
            cs = []
            for j in range(i):
                cs.append(j)
            self[cs].cu(self[i], gate.x)
        return self

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')