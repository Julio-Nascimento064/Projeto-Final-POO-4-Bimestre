from datetime import datetime


class Pessoa:
    """Classe base para representar pessoas da livraria."""

    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    def exibir_dados(self) -> str:
        return f"Nome: {self.nome} | E-mail: {self.email}"

    def atualizar_contato(self, novo_email: str):
        self.email = novo_email


class Usuario(Pessoa):
    """Representa um usuário da biblioteca que pode retirar livros."""

    def __init__(self, nome: str, matricula: int, email: str):
        super().__init__(nome, email)
        self.matricula = matricula
        self.emprestimos = []

    def solicitar_emprestimo(self, emprestimo: "Emprestimo") -> "Emprestimo":
        self.emprestimos.append(emprestimo)
        emprestimo.usuario = self
        return emprestimo

    def devolver_livro(self, emprestimo: "Emprestimo", livro: "Livro") -> str:
        if livro in emprestimo.livros:
            emprestimo.livros.remove(livro)
            livro.atualizar_status(True)
            return f"Livro '{livro.titulo}' devolvido com sucesso."
        return f"O livro '{livro.titulo}' não está neste empréstimo."

    def __str__(self) -> str:
        return f"Usuário: {self.nome} | Matrícula: {self.matricula}"


class Funcionario(Pessoa):
    """Representa o colaborador responsável pelo atendimento da livraria."""

    def __init__(self, nome: str, email: str, cargo: str):
        super().__init__(nome, email)
        self.cargo = cargo

    def registrar_emprestimo(self, usuario: Usuario, emprestimo: "Emprestimo") -> str:
        usuario.solicitar_emprestimo(emprestimo)
        return f"Empréstimo {emprestimo.numero_emprestimo} registrado para {usuario.nome}."

    def __str__(self) -> str:
        return f"Funcionário: {self.nome} | Cargo: {self.cargo}"


class Livro:
    """Representa um livro do acervo da livraria."""

    def __init__(self, titulo: str, autor: str, disponivel: bool = True):
        self.titulo = titulo
        self.autor = autor
        self.disponivel = disponivel

    def verificar_disponibilidade(self) -> bool:
        return self.disponivel

    def atualizar_status(self, disponivel: bool):
        self.disponivel = disponivel

    def __str__(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} - {self.autor} ({status})"


class Emprestimo:
    """Registra a retirada de um ou mais livros por um usuário."""

    def __init__(self, numero_emprestimo: int, data_retirada: str, usuario: Usuario = None):
        self.numero_emprestimo = numero_emprestimo
        self.data_retirada = data_retirada
        self.usuario = usuario
        self.livros = []

    def adicionar_livro(self, livro: Livro):
        if not livro.verificar_disponibilidade():
            raise ValueError(f"O livro '{livro.titulo}' não está disponível no momento.")
        self.livros.append(livro)
        livro.atualizar_status(False)

    def calcular_multa(self, dias_atraso: int = 0, taxa_diaria: float = 2.5) -> float:
        return dias_atraso * taxa_diaria

    def __str__(self) -> str:
        nomes = ", ".join(livro.titulo for livro in self.livros) if self.livros else "Nenhum livro"
        return (
            f"Empréstimo #{self.numero_emprestimo} | Data: {self.data_retirada} | "
            f"Usuário: {self.usuario.nome if self.usuario else 'Não informado'} | Livros: {nomes}"
        )


if __name__ == "__main__":
    # Instanciando objetos
    funcionario = Funcionario("Ana Souza", "ana@livraria.com", "Bibliotecária")
    usuario = Usuario("João Pedro", 202401, "joao@email.com")

    livro1 = Livro("Dom Casmurro", "Machado de Assis")
    livro2 = Livro("O Pequeno Príncipe", "Antoine de Saint-Exupéry")

    emprestimo = Emprestimo(101, datetime.today().strftime("%d/%m/%Y"), usuario)
    usuario.solicitar_emprestimo(emprestimo)
    emprestimo.adicionar_livro(livro1)
    emprestimo.adicionar_livro(livro2)

    print(funcionario.exibir_dados())
    print(usuario)
    print(emprestimo)
    print(f"Disponibilidade do livro 1: {livro1.verificar_disponibilidade()}")
    print(f"Multa estimada: R$ {emprestimo.calcular_multa(3):.2f}")

    print(usuario.devolver_livro(emprestimo, livro1))
    print(f"Disponibilidade após devolução: {livro1.verificar_disponibilidade()}")
