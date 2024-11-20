from typing import Self

class Calculator():
    def __init__(self) -> None:
        pass

    def add(self, a: float, b: float) -> float:
        return a + b

    def sub(self, a: float, b: float) -> float:
        return a - b

    def mul(self, a: float, b: float) -> float:
        return a * b
    
class String_builder():
    def __init__(self, buffer: None | str = None) -> None:
        if buffer is None:
            buffer = ""
        self.buffer = [buffer]

    def add_after(self, new: str) -> Self:
        self.buffer.append(new)
        return self

    def add_before(self, new: str)-> Self:
        self.buffer = [new] + self.buffer
        return self

    def build_string(self) -> str:
        return ''.join(self.buffer)
    
if __name__ == "__main__":
    with open("run_check.txt", "w") as f:
        f.write(String_builder().add_after("World!").add_before("Hello, ").build_string())