#This File has been abandoned as of now 





import random
import seaborn as sns
import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd


# Function to generate weather data
def generate_weather_data(start_date, end_date):
    date_range = pd.date_range(start_date, end_date)
    weather_data = []
    for date in date_range:
        weather_info = {
            'date': date.strftime('%Y-%m-%d'),
            'high_temp': high_season_temp(date),
            'low_temp': low_season_temp(date),
        }
        weather_data.append(weather_info)
    return weather_data


# Function to find the hottest day
def hottest_day(data):
    return max(data, key=lambda x: x['high_temp'])


# Function to find the coldest day
def coldest_day(data):
    return min(data, key=lambda x: x['low_temp'])


# Function to calculate average temperature
def avg_temp(data, temp_type):
    total_temp = sum(entry[temp_type] for entry in data)
    return total_temp / len(data)

def average_data(df, freq):
    num_df = df[['high_temp', 'low_temp']]
    if freq == 'W':
        num_df = num_df.resample('W').mean()
    elif freq == 'M':
        num_df = num_df.resample('M').mean()
    else:
        raise ValueError('freq must be W or M')
    print(f"Average data ({freq}): ", num_df.head())  # Debug: Print averaged data
    return num_df

# Function to define high season temperatures
def high_season_temp(date):
    month = date.month
    if month == 1:  # January
        return round(random.uniform(15, 20), 1)
    elif month == 2:  # February
        return round(random.uniform(15, 20), 1)
    elif month == 3:  # March
        return round(random.uniform(25, 30), 1)
    elif month == 4:  # April
        return round(random.uniform(30, 35), 1)
    elif month == 5:  # May
        return round(random.uniform(35, 40), 1)
    elif month == 6:  # June
        return round(random.uniform(45, 50), 1)
    elif month == 7:  # July
        return round(random.uniform(50, 55), 1)
    elif month == 8:  # August
        return round(random.uniform(45, 50), 1)
    elif month == 9:  # September
        return round(random.uniform(30, 35), 1)
    elif month == 10:  # October
        return round(random.uniform(30, 35), 1)
    elif month == 11:  # November
        return round(random.uniform(25, 30), 1)
    else:  # December
        return round(random.uniform(15, 20), 1)


# Function to define low season temperatures
def low_season_temp(date):
    month = date.month
    if month == 1:  # January
        return round(random.uniform(10, 15), 1)
    elif month == 2:  # February
        return round(random.uniform(10, 15), 1)
    elif month == 3:  # March
        return round(random.uniform(20, 25), 1)
    elif month == 4:  # April
        return round(random.uniform(25, 30), 1)
    elif month == 5:  # May
        return round(random.uniform(30, 35), 1)
    elif month == 6:  # June
        return round(random.uniform(40, 45), 1)
    elif month == 7:  # July
        return round(random.uniform(45, 50), 1)
    elif month == 8:  # August
        return round(random.uniform(40, 45), 1)
    elif month == 9:  # September
        return round(random.uniform(25, 30), 1)
    elif month == 10:  # October
        return round(random.uniform(25, 30), 1)
    elif month == 11:  # November
        return round(random.uniform(20, 25), 1)
    else:  # December
        return round(random.uniform(10, 15), 1)


# Function to clean data
def clean_data(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['high_temp'] = pd.to_numeric(df['high_temp'])
    df['low_temp'] = pd.to_numeric(df['low_temp'])
    print("Cleaned DataFrame head: ", df.head())  # Debug: Print DataFrame head
    return df


# Function to calculate average data


# Function to plot data
def ploting(average_data, title, canvas, plot_frame, theme='Light'):
    if theme == 'Dark':
        plt.style.use('dark_background')
        background_color = '#2E2E2E'
        text_color = 'white'
        grid_color = '#4F4F4F'
    else:
        plt.style.use('default')
        background_color = 'white'
        text_color = 'black'
        grid_color = '#CCCCCC'

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.set_facecolor(background_color)
    ax.figure.set_facecolor(background_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.title.set_color(text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.grid(True, color=grid_color)

    sns.lineplot(x=average_data.index, y='high_temp', data=average_data.reset_index(), marker='o', color='red', ax=ax,
                 label='High Temp')
    sns.lineplot(x=average_data.index, y='low_temp', data=average_data.reset_index(), marker='o', color='blue', ax=ax,
                 label='Low Temp')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    fig.tight_layout()

    # Remove previous canvas if it exists
    if canvas:
        canvas.get_tk_widget().destroy()

    # Embed the plot in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return canvas


# GUI setup
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Data Analysis")

        # Set theme for customtkinter
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Configure the grid layout to be expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        # Create left frame for input and buttons
        self.left_frame = ctk.CTkFrame(root)
        self.left_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_rowconfigure(3, weight=1)
        self.left_frame.grid_rowconfigure(4, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=1)

        # Create right frame for results
        self.right_frame = ctk.CTkFrame(root)
        self.right_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky='nsew')
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=3)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)

        font_style = ('Helvetica', 12)
        # Create and place labels and date entry widgets in left frame

        self.start_date_label = tk.Label(self.left_frame, text="Start Date:", font=font_style, foreground="black")
        self.start_date_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.start_date_entry = DateEntry(self.left_frame, width=12, background='darkblue', foreground='white',
                                          borderwidth=2, font=font_style)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.end_date_label = tk.Label(self.left_frame, text="End Date:", font=font_style, foreground="black")
        self.end_date_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.end_date_entry = DateEntry(self.left_frame, width=12, background='darkblue', foreground='white',
                                        borderwidth=2, font=font_style)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Create and place buttons in left frame
        self.generate_button = ctk.CTkButton(self.left_frame, text="Generate Weather Data",
                                             command=self.generate_and_load_data)
        self.generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.plot_weekly_button = ctk.CTkButton(self.left_frame, text="Plot Weekly Data", command=self.plot_weekly)
        self.plot_weekly_button.grid(row=3, column=0,columnspan=2, padx=10, pady=10, sticky='ew')

        self.plot_monthly_button = ctk.CTkButton(self.left_frame, text="Plot Monthly Data", command=self.plot_monthly)
        self.plot_monthly_button.grid(row=4, column=0,columnspan=2, padx=10, pady=10, sticky='ew')

        self.theme_toggle_button = ctk.CTkButton(self.left_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_toggle_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Labels to display results in right frame
        # Assuming you want to increase the font size to 14

        self.hottest_label = tk.Label(self.right_frame, text="Hottest Day: N/A", font=font_style, foreground="red")
        self.hottest_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.coldest_label = tk.Label(self.right_frame, text="Coldest Day: N/A", font=font_style, foreground="blue")
        self.coldest_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.avg_high_label = tk.Label(self.right_frame, text="Average High Temp: N/A", font=font_style, foreground="black")
        self.avg_high_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.avg_low_label = tk.Label(self.right_frame, text="Average Low Temp: N/A", font=font_style, foreground="black")
        self.avg_low_label.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.avg_temp_label = tk.Label(self.right_frame, text="Average Temperature: N/A", font=font_style, foreground="black")
        self.avg_temp_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Frame for plotting area
        self.plot_frame = ctk.CTkFrame(self.right_frame)
        self.plot_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Make plot_frame expandable
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)

        self.canvas = None
        self.weather_data = []
        self.df = pd.DataFrame()
        self.theme = "Light"  # Default theme
        self.current_plot = 'weekly'  # Default plot type

        # Generate and load data, then plot the weekly graph
        self.generate_and_load_data()
        self.plot_weekly()

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Light":
            self.theme = "Dark"
        else:
            self.theme = "Light"

        # Re-plot the current graph with the new theme based on the current plot type
        if self.current_plot == 'weekly':
            self.plot_weekly()
        else:
            self.plot_monthly()

    def generate_and_load_data(self):
        # Generate new weather data
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        self.weather_data = generate_weather_data(start_date, end_date)
        print("Generated weather data.")

        # Clean the weather data
        self.df = clean_data(self.weather_data)
        print("Cleaned weather data.")

        # Update labels with hottest, coldest, and average temperatures
        hottest = hottest_day(self.weather_data)
        coldest = coldest_day(self.weather_data)
        avg_high = avg_temp(self.weather_data, 'high_temp')
        avg_low = avg_temp(self.weather_data, 'low_temp')
        avg_temps = (avg_high + avg_low) / 2.0

        self.hottest_label.configure(text=f"Hottest Day: {hottest['date']} ({hottest['high_temp']}°C)")
        self.coldest_label.configure(text=f"Coldest Day: {coldest['date']} ({coldest['low_temp']}°C)")
        self.avg_high_label.configure(text=f"Average High Temp: {avg_high:.1f}°C")
        self.avg_low_label.configure(text=f"Average Low Temp: {avg_low:.1f}°C")
        self.avg_temp_label.configure(text=f"Average Temp: {avg_temps:.1f}°C")

    def plot_weekly(self):
        if not self.df.empty:
            weekly_data = average_data(self.df, 'W')
            self.canvas = ploting(weekly_data, 'Weekly Average Temperature', self.canvas, self.plot_frame, self.theme)
            self.current_plot = 'weekly'
        else:
            print("Data not loaded. Please load the data first.")

    def plot_monthly(self):
        if not self.df.empty:
            monthly_data = average_data(self.df, 'M')
            self.canvas = ploting(monthly_data, 'Monthly Average Temperature', self.canvas, self.plot_frame, self.theme)
            self.current_plot = 'monthly'
        else:
            print("Data not loaded. Please load the data first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
