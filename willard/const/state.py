import torch


class StateType:
    def ket(self, bit_array: str):
        state = torch.tensor([[1.]], dtype=torch.cfloat)
        for bit in bit_array:
            if bit == '0':
                state = torch.kron(state, torch.tensor(
                    [[1.], [0.]], dtype=torch.cfloat))
            elif bit == '1':
                state = torch.kron(state, torch.tensor(
                    [[0.], [1.]], dtype=torch.cfloat))
            else:
                raise ValueError(
                    f"bit_array should contain either '0' or '1', but {bit} has found")
        return state


state = StateType()
