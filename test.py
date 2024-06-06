import unittest
from datetime import datetime
from Interface import FilaDePrioridades

class TestFilaDePrioridades(unittest.TestCase):

    def setUp(self):
        self.fila = FilaDePrioridades()
    
    def test_adicionar_tarefa(self):
        self.fila.adicionar_tarefa("Tarefa 1", 1, "2024-06-01")
        self.assertEqual(len(self.fila.fila_pendentes), 1)
        self.assertEqual(str(self.fila.fila_pendentes[0]), "Tarefa 1 (Prioridade: 1, Prazo: 2024-06-01)")

    def test_remover_tarefa(self):
        self.fila.adicionar_tarefa("Tarefa 1", 1, "2024-06-01")
        tarefa_removida = self.fila.remover_tarefa()
        self.assertEqual(len(self.fila.fila_pendentes), 0)
        self.assertEqual(str(tarefa_removida), "Tarefa 1 (Prioridade: 1, Prazo: 2024-06-01)")
    
    def test_concluir_tarefa(self):
        self.fila.adicionar_tarefa("Tarefa 1", 1, "2024-06-01")
        tarefa_concluida = self.fila.concluir_tarefa("Tarefa 1")
        self.assertEqual(len(self.fila.fila_pendentes), 0)
        self.assertEqual(len(self.fila.tarefas_concluidas), 1)
        self.assertEqual(str(tarefa_concluida), "Tarefa 1 (Prioridade: 1, Prazo: 2024-06-01)")

    def test_pesquisar_tarefas(self):
        self.fila.adicionar_tarefa("Tarefa 1", 1, "2024-06-01")
        self.fila.adicionar_tarefa("Tarefa 2", 2, "2024-06-02")
        tarefas = self.fila.pesquisar_tarefas("Tarefa 1")
        self.assertEqual(len(tarefas), 1)
        self.assertEqual(str(tarefas[0]), "Tarefa 1 (Prioridade: 1, Prazo: 2024-06-01)")

    def test_filtrar_tarefas(self):
        self.fila.adicionar_tarefa("Tarefa 1", 1, "2024-06-01")
        self.fila.adicionar_tarefa("Tarefa 2", 2, "2024-06-02")
        tarefas_prioridade_1 = self.fila.filtrar_tarefas(prioridade=1)
        self.assertEqual(len(tarefas_prioridade_1), 1)
        self.assertEqual(str(tarefas_prioridade_1[0]), "Tarefa 1 (Prioridade: 1, Prazo: 2024-06-01)")
        
        tarefas_prazo = self.fila.filtrar_tarefas(prazo="2024-06-02")
        self.assertEqual(len(tarefas_prazo), 1)
        self.assertEqual(str(tarefas_prazo[0]), "Tarefa 2 (Prioridade: 2, Prazo: 2024-06-02)")

if __name__ == "__main__":
    unittest.main()
