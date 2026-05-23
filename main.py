from controllers.main_controller import MainController

if __name__ == "__main__":
    controller = MainController('dados_posto_combustivel.csv')
    controller.run()
