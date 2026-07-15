class AppState:
    """
    Stores the application's shared data.
    """

    def __init__(self):

        self.products = []

        self.selected_products = []

        self.downloaded_images = {}

        self.current_product = None

        self.csv_path = None