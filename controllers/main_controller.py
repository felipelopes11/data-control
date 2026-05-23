from models.data_model import DataModel
from views.dashboard_view import DashboardView

class MainController:
    def __init__(self, data_file):
        self.model = DataModel(data_file)
        self.view = DashboardView()

    def run(self):
        self.view.render_header()

        if self.model.is_empty():
            self.view.render_error("Arquivo 'dados_posto_combustivel.csv' não encontrado ou está vazio. Adicione o arquivo na raiz do projeto.")
            return

        frentistas = self.model.get_opcoes_frentistas()
        combustiveis = self.model.get_opcoes_combustiveis()

        frentista_sel, combustiveis_sel = self.view.render_sidebar(frentistas, combustiveis)

        dados_filtrados = self.model.get_dados_filtrados(frentista_sel, combustiveis_sel)

        if dados_filtrados.empty:
            self.view.render_warning("Nenhum dado encontrado para os filtros selecionados.")
        else:
            self.view.render_dashboard(dados_filtrados)
