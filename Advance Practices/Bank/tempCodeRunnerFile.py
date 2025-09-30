amount_validator = QIntValidator()
        deposittextbox.setPlaceholderText("Amount")
        deposittextbox.setInputMask("000000000;_")
        deposittextbox.setValidator(amount_validator)