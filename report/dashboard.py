from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# Import the load_model function from the utils.py file
from utils import load_model

# Import parent classes for subclassing
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)
from combined_components import FormGroup, CombinedComponent

# Create a subclass of base_components/Dropdown called ReportDropdown
class ReportDropdown(Dropdown):
    """Dropdown component for selecting report entities (employees or teams)."""

    def build_component(self, model=None, asset_id=None):
        """Build the dropdown component with a label based on the model name.

        Args:
            model: The model instance (Employee or Team)
            asset_id: Optional ID for pre-selecting an option

        Returns:
            fast_html component: The rendered dropdown component
        """
        # Set the label attribute to the model's name
        self.label = model.name if model else self.label
        # Return the output from the parent class's build_component method
        return super().build_component(model, asset_id)

    def component_data(self, model=None, asset_id=None):
        """Retrieve data for the dropdown from the model's names method.

        Args:
            model: The model instance (Employee or Team)
            asset_id: Optional ID for pre-selecting an option

        Returns:
            list: List of tuples containing names and IDs
        """
        # Call the model's names method to get names and IDs
        if model:
            return model.names()
        return []

# Create a subclass of base_components/BaseComponent called Header
class Header(BaseComponent):
    """Header component displaying the model's name."""

    def build_component(self, model=None, asset_id=None):
        """Build an H1 component with the model's name.

        Args:
            model: The model instance (Employee or Team)
            asset_id: Optional ID (not used in this component)

        Returns:
            fast_html component: H1 element with the model's name
        """
        # Return an H1 component containing the model's name attribute
        return H1(model.name if model else "Report")

# Create a subclass of base_components/MatplotlibViz called LineChart
class LineChart(MatplotlibViz):
    """Line chart visualizing cumulative positive and negative event counts."""

    def visualization(self, model, asset_id):
        """Generate a line chart of cumulative event counts.

        Args:
            model: The model instance (Employee or Team)
            asset_id: The ID to filter event counts

        Returns:
            matplotlib.figure.Figure: The generated line chart
        """
        # Pass asset_id to the model's event_counts method
        df = model.event_counts(asset_id)
        
        # Use pandas .fillna to fill nulls with 0
        df = df.fillna(0)
        
        # Set the date column as the index
        df = df.set_index('event_date')
        
        # Sort the index
        df = df.sort_index()
        
        # Use .cumsum to get cumulative counts
        df = df.cumsum()
        
        # Set dataframe columns to ['Positive', 'Negative']
        df.columns = ['Positive', 'Negative']
        
        # Initialize a matplotlib subplot
        fig, ax = plt.subplots()
        
        # Plot the cumulative counts
        df.plot(ax=ax)
        
        # Set axis styling with black border and font color
        self.set_axis_styling(ax=ax, border_color='black', font_color='black')
        
        # Set title and labels
        ax.set_title('Cumulative Event Counts')
        ax.set_xlabel('Date')
        ax.set_ylabel('Event Count')
        
        return fig

# Create a subclass of base_components/MatplotlibViz called BarChart
class BarChart(MatplotlibViz):
    """Bar chart visualizing predicted recruitment risk."""
    
    # Create a predictor class attribute using load_model
    predictor = load_model()

    def visualization(self, model, asset_id):
        """Generate a bar chart of predicted recruitment risk.

        Args:
            model: The model instance (Employee or Team)
            asset_id: The ID to filter model data

        Returns:
            matplotlib.figure.Figure: The generated bar chart
        """
        # Pass asset_id to the model's model_data method
        data = model.model_data(asset_id)
        
        # Pass data to the predictor's predict_proba method
        predictions = self.predictor.predict_proba(data)
        
        # Index the second column of predict_proba output
        prob = predictions[:, 1]
        
        # Set pred based on model name
        if model.name == "team":
            pred = prob.mean()  # Mean for team
        else:
            pred = prob[0]  # First value for employee
        
        # Initialize a matplotlib subplot
        fig, ax = plt.subplots()
        
        # Run provided code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # Set axis styling with black border and font color
        self.set_axis_styling(ax=ax, border_color='black', font_color='black')
        
        return fig

# Create a subclass of combined_components/CombinedComponent called Visualizations
class Visualizations(CombinedComponent):
    """Component combining LineChart and BarChart visualizations."""
    
    # Set children to instances of LineChart and BarChart
    children = [LineChart(), BarChart()]
    
    outer_div_type = Div(cls='grid')

# Create a subclass of base_components/DataTable called NotesTable
class NotesTable(DataTable):
    """Table component displaying notes data."""

    def component_data(self, model=None, entity_id=None):
        """Retrieve notes data for the given model and entity ID.

        Args:
            model: The model instance (Employee or Team)
            entity_id: The ID to filter notes

        Returns:
            pd.DataFrame: DataFrame containing notes data
        """
        # Pass entity_id to the model's notes method
        if model and entity_id:
            return model.notes(entity_id)
        return pd.DataFrame()

# Provided DashboardFilters class (unchanged)
class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"
    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]

# Create a subclass of CombinedComponent called Report
class Report(CombinedComponent):
    """Main report component combining header, filters, visualizations, and notes."""
    
    # Set children to instances of Header, DashboardFilters, Visualizations, and NotesTable
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# Initialize a fasthtml app
app = FastAPI()

# Initialize the Report class
report = Report()

# Create a route for a GET request to the root
@app.get("/")
def get_root():
    """Render the report for a default employee with ID 1."""
    return report(Employee(), 1)

# Create a route for a GET request with parameterized employee ID
@app.get("/employee/{id}")
def get_employee(id: str):
    """Render the report for an employee with the specified ID.

    Args:
        id (str): The employee ID

    Returns:
        fast_html component: The rendered report
    """
    return report(Employee(), int(id))

# Create a route for a GET request with parameterized team ID
@app.get("/team/{id}")
def get_team(id: str):
    """Render the report for a team with the specified ID.

    Args:
        id (str): The team ID

    Returns:
        fast_html component: The rendered report
    """
    return report(Team(), int(id))

# Keep the below code unchanged
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

serve()
