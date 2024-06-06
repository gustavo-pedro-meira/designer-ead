import tkinter as tk
from tkinter import ttk, messagebox
import heapq

class Tarefa:
    def __init__(self, descricao: str, prioridade: int, prazo: str):
        self.descricao = descricao
        self.prioridade = prioridade
        self.prazo = prazo

    def __lt__(self, other):
        return self.prioridade > other.prioridade

    def __str__(self):
        return f"{self.descricao} (Prioridade: {self.prioridade}, Prazo: {self.prazo})"

class FilaDePrioridades:
    def __init__(self):
        self.fila_pendentes = []
        self.tarefas_concluidas = []

    def adicionar_tarefa(self, descricao: str, prioridade: int, prazo: str):
        tarefa = Tarefa(descricao, prioridade, prazo)
        heapq.heappush(self.fila_pendentes, tarefa)

    def remover_tarefa(self):
        if self.fila_pendentes:
            return heapq.heappop(self.fila_pendentes)
        else:
            raise IndexError("A fila de pendentes está vazia")

    def concluir_tarefa(self, descricao: str):
        for i, tarefa in enumerate(self.fila_pendentes):
            if tarefa.descricao == descricao:
                concluida = self.fila_pendentes.pop(i)
                heapq.heapify(self.fila_pendentes)
                self.tarefas_concluidas.append(concluida)
                return concluida
        raise ValueError("Tarefa não encontrada na fila de pendentes")

    def pesquisar_tarefas(self, termo: str):
        return [tarefa for tarefa in self.fila_pendentes if termo in tarefa.descricao]

    def filtrar_tarefas(self, prioridade: int = None, prazo: str = None):
        result = self.fila_pendentes[:]
        if prioridade is not None:
            result = [tarefa for tarefa in result if tarefa.prioridade == prioridade]
        if prazo is not None:
            result = [tarefa for tarefa in result if tarefa.prazo == prazo]
        return result

class App:
    def __init__(self, root):
        self.fila = FilaDePrioridades()
        self.root = root
        self.root.title("Gerenciador de Tarefas")

        # Frames
        self.frame_entrada = ttk.Frame(root)
        self.frame_entrada.pack(pady=10)

        self.frame_botoes = ttk.Frame(root)
        self.frame_botoes.pack(pady=10)

        self.frame_lista = ttk.Frame(root)
        self.frame_lista.pack(pady=10)

        # Entrada de Tarefa
        self.label_descricao = ttk.Label(self.frame_entrada, text="Descrição:")
        self.label_descricao.grid(row=0, column=0, padx=5, pady=5)
        self.entry_descricao = ttk.Entry(self.frame_entrada, width=50)
        self.entry_descricao.grid(row=0, column=1, padx=5, pady=5)

        self.label_prioridade = ttk.Label(self.frame_entrada, text="Prioridade:")
        self.label_prioridade.grid(row=1, column=0, padx=5, pady=5)
        self.combo_prioridade = ttk.Combobox(self.frame_entrada, values=[1, 2, 3, 4])
        self.combo_prioridade.grid(row=1, column=1, padx=5, pady=5)

        self.label_prazo = ttk.Label(self.frame_entrada, text="Prazo:")
        self.label_prazo.grid(row=2, column=0, padx=5, pady=5)
        self.entry_prazo = ttk.Entry(self.frame_entrada)
        self.entry_prazo.grid(row=2, column=1, padx=5, pady=5)

        # Botões
        self.btn_adicionar = ttk.Button(self.frame_botoes, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.btn_adicionar.grid(row=0, column=0, padx=5, pady=5)

        self.btn_remover = ttk.Button(self.frame_botoes, text="Remover Tarefa", command=self.remover_tarefa)
        self.btn_remover.grid(row=0, column=1, padx=5, pady=5)

        self.btn_concluir = ttk.Button(self.frame_botoes, text="Concluir Tarefa", command=self.concluir_tarefa)
        self.btn_concluir.grid(row=0, column=2, padx=5, pady=5)

        self.btn_pesquisar = ttk.Button(self.frame_botoes, text="Pesquisar Tarefa", command=self.pesquisar_tarefas)
        self.btn_pesquisar.grid(row=0, column=3, padx=5, pady=5)

        self.btn_filtrar = ttk.Button(self.frame_botoes, text="Filtrar Tarefas", command=self.filtrar_tarefas)
        self.btn_filtrar.grid(row=0, column=4, padx=5, pady=5)

        # Lista de Tarefas
        self.label_pendentes = ttk.Label(self.frame_lista, text="Tarefas Pendentes:")
        self.label_pendentes.pack()
        self.listbox_pendentes = tk.Listbox(self.frame_lista, width=100)
        self.listbox_pendentes.pack(pady=5)

        self.label_concluidas = ttk.Label(self.frame_lista, text="Tarefas Concluídas:")
        self.label_concluidas.pack()
        self.listbox_concluidas = tk.Listbox(self.frame_lista, width=100)
        self.listbox_concluidas.pack(pady=5)

    def adicionar_tarefa(self):
        descricao = self.entry_descricao.get()
        prioridade = self.combo_prioridade.get()
        prazo = self.entry_prazo.get()
        if descricao and prioridade and prazo:
            try:
                prioridade = int(prioridade)
                self.fila.adicionar_tarefa(descricao, prioridade, prazo)
                self.entry_descricao.delete(0, tk.END)
                self.combo_prioridade.set('')
                self.entry_prazo.delete(0, tk.END)
                self.atualizar_listas()
            except ValueError:
                messagebox.showwarning("Atenção", "Prioridade deve ser um número inteiro")
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios")

    def remover_tarefa(self):
        try:
            tarefa = self.fila.remover_tarefa()
            self.atualizar_listas()
            messagebox.showinfo("Sucesso", f"Tarefa removida: {tarefa}")
        except IndexError:
            messagebox.showwarning("Atenção", "Não há tarefas para remover")

    def concluir_tarefa(self):
        try:
            # Remover a tarefa diretamente da fila de pendentes
            tarefa_concluida = self.fila.remover_tarefa()
            # Adicionar a tarefa concluída à lista de tarefas concluídas
            self.fila.tarefas_concluidas.append(tarefa_concluida)
            # Atualizar as listas
            self.atualizar_listas()
            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Tarefa concluída: {tarefa_concluida}")
        except IndexError:
            # Exibir aviso se não houver tarefas na fila de pendentes
            messagebox.showwarning("Atenção", "Não há tarefas para concluir")




    def pesquisar_tarefas(self):
        termo = self.entry_descricao.get()
        tarefas = self.fila.pesquisar_tarefas(termo)
        self.listbox_pendentes.delete(0, tk.END)
        for tarefa in tarefas:
            self.listbox_pendentes.insert(tk.END, tarefa)

    def filtrar_tarefas(self):
        prioridade = self.combo_prioridade.get()
        prazo = self.entry_prazo.get()
        if prioridade:
            prioridade = int(prioridade)
        else:
            prioridade = None
        tarefas = self.fila.filtrar_tarefas(prioridade, prazo)
        self.listbox_pendentes.delete(0, tk.END)
        for tarefa in tarefas:
            self.listbox_pendentes.insert(tk.END, tarefa)

    def atualizar_listas(self):
        self.listbox_pendentes.delete(0, tk.END)
        for tarefa in self.fila.fila_pendentes:
            self.listbox_pendentes.insert(tk.END, tarefa)
        
        self.listbox_concluidas.delete(0, tk.END)
        for tarefa in self.fila.tarefas_concluidas:
            self.listbox_concluidas.insert(tk.END, tarefa)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()