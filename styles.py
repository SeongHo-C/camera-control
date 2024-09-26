def button_style(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: white; 
            color: black;               
            border: 1px solid gray;   
            border-radius: 5px;          
            padding: 10px;           
        }
        QPushButton:hover {
            background-color: gray;
            color: white;  
        }
    """)