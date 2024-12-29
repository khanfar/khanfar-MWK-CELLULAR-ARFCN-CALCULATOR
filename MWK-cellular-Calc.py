import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple, Optional

class NetworkCalculator:
    """Handles cellular network frequency calculations."""
    
    NETWORK_RANGES = {
        'GSM 900': [(1, 124), (128, 251)],
        'GSM 1800': [(512, 885), (1024, 1885)],
        'UMTS 2100': [(10562, 10687)],
        'LTE 1800': [(300, 379)]
    }

    CHANNEL_SPACING = {
        'GSM 900': 0.2,  # MHz
        'GSM 1800': 0.2,  # MHz
        'UMTS 2100': 5.0,  # MHz
        'LTE 1800': 0.1   # MHz
    }

    NETWORK_CAPABILITIES = {
        'GSM 900': {
            'Technology': '2G',
            'Max Data Rate': '115 Kbps (GPRS), 384 Kbps (EDGE)',
            'Features': 'Voice calls, SMS, Basic data',
            'Modulation': 'GMSK, 8PSK (EDGE)'
        },
        'GSM 1800': {
            'Technology': '2G',
            'Max Data Rate': '115 Kbps (GPRS), 384 Kbps (EDGE)',
            'Features': 'Voice calls, SMS, Basic data',
            'Modulation': 'GMSK, 8PSK (EDGE)'
        },
        'UMTS 2100': {
            'Technology': '3G',
            'Max Data Rate': '42 Mbps (DC-HSPA+)',
            'Features': 'Video calls, High-speed data, Enhanced security',
            'Modulation': 'QPSK, 16QAM'
        },
        'LTE 1800': {
            'Technology': '4G',
            'Max Data Rate': 'Up to 150 Mbps',
            'Features': 'High-speed data, VoLTE, Low latency',
            'Modulation': 'QPSK, 16QAM, 64QAM'
        }
    }

    @staticmethod
    def calculate_gsm900(arfcn: int) -> Tuple[float, float]:
        """Calculate GSM 900 frequencies."""
        if 1 <= arfcn <= 124:
            base_arfcn = arfcn - 1
        else:
            base_arfcn = arfcn - 128
        uplink = 880.2 + base_arfcn * 0.2
        downlink = 925.2 + base_arfcn * 0.2
        return uplink, downlink

    @staticmethod
    def calculate_gsm1800(arfcn: int) -> Tuple[float, float]:
        """Calculate GSM 1800 frequencies."""
        if 512 <= arfcn <= 885:
            base_arfcn = arfcn - 512
        else:
            base_arfcn = arfcn - 1024
        uplink = 1710 + base_arfcn * 0.2
        downlink = 1805 + base_arfcn * 0.2
        return uplink, downlink

    @staticmethod
    def calculate_umts2100(arfcn: int) -> Tuple[float, float]:
        """Calculate UMTS 2100 frequencies."""
        base_arfcn = arfcn - 10562
        uplink = 1922.4 + base_arfcn * 0.2
        downlink = 2112.4 + base_arfcn * 0.2
        return uplink, downlink

    @staticmethod
    def calculate_lte1800(arfcn: int) -> Tuple[float, float]:
        """Calculate LTE 1800 frequencies."""
        base_arfcn = arfcn - 300
        uplink = 1710 + base_arfcn * 0.1
        downlink = 1805 + base_arfcn * 0.1
        return uplink, downlink

    @classmethod
    def detect_network(cls, arfcn: int) -> Optional[str]:
        """Detect network type based on ARFCN."""
        for network, ranges in cls.NETWORK_RANGES.items():
            for start, end in ranges:
                if start <= arfcn <= end:
                    return network
        return None

    @classmethod
    def calculate_frequencies(cls, arfcn: int) -> Tuple[float, float, str]:
        """Calculate frequencies for given ARFCN."""
        network = cls.detect_network(arfcn)
        if not network:
            raise ValueError(f"ARFCN {arfcn} is not in any known network range")

        if network == "GSM 900":
            uplink, downlink = cls.calculate_gsm900(arfcn)
        elif network == "GSM 1800":
            uplink, downlink = cls.calculate_gsm1800(arfcn)
        elif network == "UMTS 2100":
            uplink, downlink = cls.calculate_umts2100(arfcn)
        else:  # LTE 1800
            uplink, downlink = cls.calculate_lte1800(arfcn)

        return uplink, downlink, network

    @staticmethod
    def calculate_center_frequency(uplink: float, downlink: float) -> float:
        """Calculate center frequency between uplink and downlink."""
        return (uplink + downlink) / 2

    @classmethod
    def get_channel_spacing(cls, network: str) -> float:
        """Get channel spacing for the network type."""
        return cls.CHANNEL_SPACING.get(network, 0.0)

    @classmethod
    def get_network_capabilities(cls, network: str) -> dict:
        """Get network capabilities and features."""
        return cls.NETWORK_CAPABILITIES.get(network, {})

class CellularCalculatorGUI:
    """GUI for the Cellular Network Calculator."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Cellular ARFCN Calculator")
        
        # Set window size and position
        window_width = 600
        window_height = 900
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.window.minsize(400, 500)  # Allow smaller window size
        
        # Create outer container
        self.outer_frame = ttk.Frame(self.window)
        self.outer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add canvas and scrollbar
        self.canvas = tk.Canvas(self.outer_frame)
        self.scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        
        # Create main container
        self.main_container = ttk.Frame(self.canvas)
        
        # Configure canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        
        # Configure scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind events
        self.main_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.window.bind("<MouseWheel>", self.on_mousewheel)
        
        self.setup_gui()
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        # Scrollbar starts hidden
        self.update_scrollbar()

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.update_scrollbar()

    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        self.update_scrollbar()

    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.scrollbar.winfo_viewable():  # Only scroll if scrollbar is visible
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_scrollbar(self):
        """Show or hide scrollbar based on content height"""
        if self.main_container.winfo_reqheight() > self.canvas.winfo_height():
            self.scrollbar.pack(side="right", fill="y")
        else:
            self.scrollbar.pack_forget()

    def setup_gui(self):
        """Set up the GUI elements."""
        # Style configuration
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Result.TLabel', font=('Helvetica', 12))
        
        # Title
        title = ttk.Label(
            self.main_container, 
            text="MWK Cellular Network ARFCN Calculator",
            style='Title.TLabel'
        )
        title.pack(pady=20)

        # Network ranges info
        self.create_network_info_frame()

        # Calculator frame
        self.create_calculator_frame()

        # Results frame
        self.create_results_frame()

    def create_network_info_frame(self):
        """Create frame showing network ranges."""
        info_frame = ttk.LabelFrame(self.main_container, text="Network Ranges")
        info_frame.pack(padx=10, pady=10, fill="x")

        for network, ranges in NetworkCalculator.NETWORK_RANGES.items():
            range_text = ", ".join([f"{start}-{end}" for start, end in ranges])
            ttk.Label(
                info_frame,
                text=f"{network}: {range_text}"
            ).pack(padx=5, pady=2, anchor="w")

    def create_calculator_frame(self):
        """Create the calculator input frame."""
        calc_frame = ttk.Frame(self.main_container)
        calc_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(calc_frame, text="Enter ARFCN:").pack(pady=5)
        
        self.arfcn_entry = ttk.Entry(calc_frame, width=20)
        self.arfcn_entry.pack(pady=5)
        
        ttk.Button(
            calc_frame,
            text="Calculate",
            command=self.calculate
        ).pack(pady=10)

    def create_results_frame(self):
        """Create the results display frame."""
        results_frame = ttk.LabelFrame(self.main_container, text="Results")
        results_frame.pack(padx=10, pady=10, fill="x")

        self.uplink_label = ttk.Label(
            results_frame,
            text="Uplink Frequency: -- MHz",
            style='Result.TLabel'
        )
        self.uplink_label.pack(pady=5)

        self.downlink_label = ttk.Label(
            results_frame,
            text="Downlink Frequency: -- MHz",
            style='Result.TLabel'
        )
        self.downlink_label.pack(pady=5)

        self.center_freq_label = ttk.Label(
            results_frame,
            text="Center Frequency: -- MHz",
            style='Result.TLabel'
        )
        self.center_freq_label.pack(pady=5)

        self.channel_spacing_label = ttk.Label(
            results_frame,
            text="Channel Spacing: -- MHz",
            style='Result.TLabel'
        )
        self.channel_spacing_label.pack(pady=5)

        self.network_label = ttk.Label(
            results_frame,
            text="Network Type: --",
            style='Result.TLabel'
        )
        self.network_label.pack(pady=5)

        # Network capabilities frame
        capabilities_frame = ttk.LabelFrame(self.main_container, text="Network Capabilities")
        capabilities_frame.pack(padx=10, pady=10, fill="x")

        self.tech_label = ttk.Label(
            capabilities_frame,
            text="Technology: --",
            style='Result.TLabel'
        )
        self.tech_label.pack(pady=5)

        self.data_rate_label = ttk.Label(
            capabilities_frame,
            text="Max Data Rate: --",
            style='Result.TLabel'
        )
        self.data_rate_label.pack(pady=5)

        self.features_label = ttk.Label(
            capabilities_frame,
            text="Features: --",
            style='Result.TLabel'
        )
        self.features_label.pack(pady=5)

        self.modulation_label = ttk.Label(
            capabilities_frame,
            text="Modulation: --",
            style='Result.TLabel'
        )
        self.modulation_label.pack(pady=5)

        # Add dialer codes info frame
        dialer_frame = ttk.LabelFrame(self.main_container, text="Network Info Dialer Codes")
        dialer_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(
            dialer_frame,
            text="Android: *#*#4636#*#*",
            style='Result.TLabel'
        ).pack(pady=5)

        ttk.Label(
            dialer_frame,
            text="iPhone: *3001#12345#*",
            style='Result.TLabel'
        ).pack(pady=5)

    def calculate(self):
        """Handle calculation button click."""
        try:
            arfcn = int(self.arfcn_entry.get())
            uplink, downlink, network = NetworkCalculator.calculate_frequencies(arfcn)
            
            # Calculate center frequency and get channel spacing
            center_freq = NetworkCalculator.calculate_center_frequency(uplink, downlink)
            channel_spacing = NetworkCalculator.get_channel_spacing(network)
            capabilities = NetworkCalculator.get_network_capabilities(network)
            
            self.uplink_label.config(text=f"Uplink Frequency: {uplink:.3f} MHz")
            self.downlink_label.config(text=f"Downlink Frequency: {downlink:.3f} MHz")
            self.center_freq_label.config(text=f"Center Frequency: {center_freq:.3f} MHz")
            self.channel_spacing_label.config(text=f"Channel Spacing: {channel_spacing} MHz")
            self.network_label.config(text=f"Network Type: {network}")
            
            # Update network capabilities
            self.tech_label.config(text=f"Technology: {capabilities.get('Technology', '--')}")
            self.data_rate_label.config(text=f"Max Data Rate: {capabilities.get('Max Data Rate', '--')}")
            self.features_label.config(text=f"Features: {capabilities.get('Features', '--')}")
            self.modulation_label.config(text=f"Modulation: {capabilities.get('Modulation', '--')}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def run(self):
        """Start the GUI application."""
        self.window.mainloop()

if __name__ == "__main__":
    app = CellularCalculatorGUI()
    app.run()