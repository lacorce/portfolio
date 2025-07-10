def create_report_chart(stats: dict) -> str:
    import matplotlib.pyplot as plt
    import tempfile

    income = stats.get('income', {})
    expense = stats.get('expense', {})

    income_categories = []
    income_values = []
    for currency, cat_dict in income.items():
        for cat, val in cat_dict.items():
            income_categories.append(f"{cat} ({currency})")
            income_values.append(float(val))

    expense_categories = []
    expense_values = []
    for currency, cat_dict in expense.items():
        for cat, val in cat_dict.items():
            expense_categories.append(f"{cat} ({currency})")
            expense_values.append(float(val))

    total_categories = income_categories + expense_categories
    total_values = income_values + expense_values

    if not total_categories:
        total_categories = ['Нет данных']
        total_values = [0]

    y_positions = range(len(total_categories))

    fig, ax = plt.subplots(figsize=(10, max(len(total_categories)*0.5, 2)))
    width = 0.4

    if income_values:
        ax.barh(
            y_positions[:len(income_values)],
            income_values,
            height=width,
            color='green',
            label='Доходы'
        )

    if expense_values:
        ax.barh(
            [y + width for y in y_positions[len(income_values):]],
            expense_values,
            height=width,
            color='red',
            label='Расходы'
        )

    ax.set_yticks(
        [y + width / 2 for y in y_positions]
    )
    ax.set_yticklabels(total_categories)

    ax.set_xlabel('Сумма')
    ax.set_title('Отчёт по доходам и расходам')
    ax.legend()
    plt.tight_layout()

    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(tmp_file.name)
    plt.close()
    return tmp_file.name
