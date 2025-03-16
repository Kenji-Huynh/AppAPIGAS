# ui_factory.py
import tkinter as tk
from tkinter import ttk, scrolledtext

class UIFactory:
    """Factory class for creating consistent UI elements"""
    
    @staticmethod
    def create_tab(notebook, title):
        """Create a new tab in the notebook"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=title)
        return tab
    
    @staticmethod
    def create_button(parent, text, command, width=None):
        """Create a standard button"""
        button = ttk.Button(parent, text=text, command=command)
        if width:
            button.config(width=width)
        return button
    
    @staticmethod
    def create_label(parent, text, font=None, anchor=None, **kwargs):
        """Create a standard label"""
        label = ttk.Label(parent, text=text, **kwargs)
        if font:
            label.config(font=font)
        if anchor:
            label.config(anchor=anchor)
        return label
    
    @staticmethod
    def create_entry(parent, width=None, show=None, textvariable=None):
        """Create a standard entry field"""
        entry = ttk.Entry(parent)
        if width:
            entry.config(width=width)
        if show:
            entry.config(show=show)
        if textvariable:
            entry.config(textvariable=textvariable)
        return entry
    
    @staticmethod
    def create_text_area(parent, height=None, width=None, wrap=tk.WORD):
        """Create a standard text area"""
        text = scrolledtext.ScrolledText(parent, wrap=wrap)
        if height:
            text.config(height=height)
        if width:
            text.config(width=width)
        return text
    
    @staticmethod
    def create_combobox(parent, values=None, state="readonly", width=None):
        """Create a standard combobox"""
        combo = ttk.Combobox(parent, state=state)
        if values:
            combo["values"] = values
        if width:
            combo.config(width=width)
        return combo

    @staticmethod
    def create_frame(parent, padding=None, borderwidth=None):
        """Create a standard frame"""
        frame = ttk.Frame(parent)
        if padding:
            frame.config(padding=padding)
        if borderwidth:
            frame.config(borderwidth=borderwidth)
        return frame
    
    @staticmethod
    def create_labeled_frame(parent, text, padding=None):
        """Create a labeled frame"""
        frame = ttk.LabelFrame(parent, text=text)
        if padding:
            frame.config(padding=padding)
        return frame
    
    @staticmethod
    def create_progress_bar(parent, mode="determinate", length=None):
        """Create a standard progress bar"""
        progress = ttk.Progressbar(parent, mode=mode)
        if length:
            progress.config(length=length)
        return progress
    
    @staticmethod
    def create_checkbox(parent, text, variable):
        """Create a standard checkbox"""
        checkbox = ttk.Checkbutton(parent, text=text, variable=variable)
        return checkbox
    
    @staticmethod
    def create_radio_button(parent, text, variable, value):
        """Create a standard radio button"""
        radio = ttk.Radiobutton(parent, text=text, variable=variable, value=value)
        return radio
    
    @staticmethod
    def create_slider(parent, from_val, to_val, variable=None, orient=tk.HORIZONTAL):
        """Create a standard slider"""
        slider = ttk.Scale(parent, from_=from_val, to=to_val, orient=orient)
        if variable:
            slider.config(variable=variable)
        return slider
    
    @staticmethod
    def create_status_bar(parent):
        """Create a status bar at the bottom of the window"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        status_label = ttk.Label(status_frame, text="Sẵn sàng", anchor=tk.W, 
                                relief=tk.SUNKEN, padding=(2, 0))
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        return status_label

