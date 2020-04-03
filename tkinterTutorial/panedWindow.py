# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:53:15 2020

@author: FBA_S
"""

import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()

# the main window is divided into left and right sections,
# and the sidebar is divided into a top and bottom section.
pw = ttk.PanedWindow(orient="horizontal")

pwSidebar = ttk.PanedWindow(pw, orient="vertical")
main = tk.Frame(pw, width=400, height=400, background="black")
frmSidebarTop = tk.Frame(pwSidebar, width=200, height=200, background="gray")
frmSidebarBottom = tk.Frame(pwSidebar, width=200, height=200, background="white")

# add the paned window to the root
pw.pack(fill="both", expand=True)

# add the sidebar and main area to the main paned window
pw.add(pwSidebar)
pw.add(main)

# add the top and bottom to the pwSidebar
pwSidebar.add(frmSidebarTop)
pwSidebar.add(frmSidebarBottom)

root.mainloop()