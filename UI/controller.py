import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._current_year = None
        self._current_shape = None

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO

        years = self._model.get_years()

        if years:
            for year in years:
                self._view.dd_year.options.append(ft.dropdown.Option(year))
        else:
            self._view.show_alert("Errore nel caricamento degli anni.")

        self._view.update()

    def on_year_change(self, e):

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_2.controls.clear()

        selected_option = e.control.value
        if not selected_option:
            self._current_year = None
            self._view.show_alert("Errore nella selezione dell'anno.")
            return

        self._current_year = selected_option

        self._view.dd_shape.disabled = False

        shapes = self._model.get_shapes(self._current_year)

        if shapes:
            for shape in shapes:
                self._view.dd_shape.options.append(ft.dropdown.Option(shape))
        else:
            self._view.show_alert("Errore nel caricamento delle forme.")

        self._view.update()

    def on_shape_change(self, e):

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_2.controls.clear()

        selected_option = e.control.value
        if not selected_option:
            self._current_shape = None
            self._view.show_alert("Errore nella selezione della forma.")
            return

        self._current_shape = selected_option

        self._view.pulsante_graph.disabled = False

        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO

        self._view.lista_visualizzazione_1.controls.clear()

        self._model.build_graph(self._current_shape, self._current_year)
        self._model.add_distance_grafo()
        num_nodes, num_edges = self._model.get_num_nodes_num_edges()
        top = self._model.sum_weights_nodes()

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di vertici: {num_nodes} | Numero di archi: {num_edges}'))
        for item in top.keys():
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Nodo {item.id}, somma pesi su archi = {top[item]}'))

        self._view.pulsante_path.disabled = False

        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

        self._view.lista_visualizzazione_2.controls.clear()

        nodes = self._model.get_nodes()

        distanze = []
        diz = {}
        for n in nodes:
            path, distanza = self._model.definitivo(n)
            diz[distanza] = path
            distanze.append(distanza)

        best_dist = max(distanze)

        best_path = diz[best_dist]

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Peso cammino massimo: {best_dist}'))

        for item in best_path.keys():
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'{item[0].id} --> {item[1].id}: weight {best_path[item][0]}, distance {best_path[item][1]}'))

        self._view.update()


