import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import random
import csv


class RegionalDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм 1: Анализ регионального распределения")
        self.root.geometry("1000x700")

        # Центрируем окно
        self.center_window()

        # Создаем демо-базу
        self.create_demo_database()

        # Подключаемся к базе
        self.conn = sqlite3.connect("regional_analysis.db")
        self.cursor = self.conn.cursor()

        # Настройка стилей
        self.setup_styles()

        # Создаем интерфейс
        self.create_widgets()

        # Загружаем данные
        self.load_data()

    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = 1000
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        """Настройка стилей для красивого интерфейса"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Green.TButton', background='#4CAF50', foreground='white')
        style.configure('Blue.TButton', background='#3498db', foreground='white')

    def create_demo_database(self):
        """Создание демонстрационной базы данных"""
        conn = sqlite3.connect("regional_analysis.db")
        cursor = conn.cursor()

        # Создаем таблицу клиентов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            registration_date DATE,
            total_purchases REAL
        )
        ''')

        # Проверяем, есть ли данные
        cursor.execute("SELECT COUNT(*) FROM clients")
        if cursor.fetchone()[0] == 0:
            # Добавляем демо-данные
            regions = [
                ('Москва', 120),
                ('Санкт-Петербург', 85),
                ('Новосибирск', 45),
                ('Екатеринбург', 38),
                ('Казань', 32),
                ('Нижний Новгород', 28),
                ('Краснодар', 25),
                ('Сочи', 18),
                ('Владивосток', 15),
                ('Калининград', 12),
                ('Ростов-на-Дону', 20),
                ('Уфа', 16),
                ('Волгоград', 14),
                ('Пермь', 13),
                ('Омск', 11)
            ]

            client_id = 1
            for region_name, count in regions:
                for i in range(count):
                    name = f"Клиент_{client_id}"
                    date = datetime.now() - timedelta(days=random.randint(0, 365))
                    purchases = random.randint(1000, 50000)

                    cursor.execute(
                        "INSERT INTO clients (name, region, registration_date, total_purchases) VALUES (?, ?, ?, ?)",
                        (name, region_name, date.date(), purchases)
                    )
                    client_id += 1

            print(f"✅ Создано {client_id - 1} демо-клиентов в {len(regions)} регионах")

        conn.commit()
        conn.close()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="📊 АНАЛИЗ РАСПРЕДЕЛЕНИЯ КЛИЕНТОВ ПО РЕГИОНАМ",
            style='Title.TLabel'
        )
        title_label.pack(pady=10)

        # Фрейм управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        # Кнопки управления
        buttons = [
            ("🔄 Обновить данные", self.load_data, "Blue.TButton"),
            ("📊 Круговая диаграмма", self.show_pie_chart, "Blue.TButton"),
            ("📈 Столбчатая диаграмма", self.show_bar_chart, "Blue.TButton"),
            ("📄 Экспорт в CSV", self.export_to_csv, "Green.TButton"),
            ("🧹 Очистить таблицу", self.clear_table, ""),
            ("ℹ️ Помощь", self.show_help, "")
        ]

        for text, command, style in buttons:
            if style:
                btn = ttk.Button(control_frame, text=text, command=command, style=style)
            else:
                btn = ttk.Button(control_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5)

        # Панель с результатами
        results_frame = ttk.LabelFrame(main_frame, text="Результаты анализа", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Создаем таблицу для отображения данных
        self.create_table(results_frame)

        # Панель статистики
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)

        self.stats_label = ttk.Label(
            stats_frame,
            text="",
            font=('Arial', 10, 'bold')
        )
        self.stats_label.pack()

    def create_table(self, parent):
        """Создание таблицы для отображения данных"""
        # Создаем Treeview с полосой прокрутки
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Определяем столбцы
        columns = ("№", "Регион", "Кол-во клиентов", "Доля (%)", "Сумма покупок", "Сегмент")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Настраиваем заголовки
        col_widths = [50, 180, 120, 100, 150, 100]
        for idx, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[idx], anchor="center")

        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_data(self):
        """Загрузка и отображение данных"""
        try:
            # Выполняем SQL-запрос для анализа
            query = """
            SELECT 
                region,
                COUNT(*) as client_count,
                SUM(total_purchases) as total_sales,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 2) as percentage
            FROM clients
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region
            ORDER BY client_count DESC
            """

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                messagebox.showinfo("Нет данных", "В базе данных нет клиентов для анализа")
                return

            # Очищаем таблицу
            self.clear_table()

            # Заполняем таблицу
            total_clients = sum(row[1] for row in results)
            total_sales = sum(row[2] for row in results)

            for idx, (region, count, sales, percentage) in enumerate(results, 1):
                # Определяем сегмент
                if percentage > 15:
                    segment = "🔴 Высокий"
                    segment_color = "red"
                elif percentage > 5:
                    segment = "🟡 Средний"
                    segment_color = "orange"
                else:
                    segment = "🟢 Низкий"
                    segment_color = "green"

                self.tree.insert("", "end", values=(
                    idx,
                    region,
                    f"{count:,}".replace(",", " "),
                    f"{percentage}%",
                    f"{sales:,.0f} ₽".replace(",", " "),
                    segment
                ))

            # Обновляем статистику
            avg_per_region = total_clients / len(results) if results else 0
            avg_sales_per_region = total_sales / len(results) if results else 0

            stats_text = f"""
            📊 СТАТИСТИКА: 
            Всего клиентов: {total_clients:,} | Регионов: {len(results)} 
            Среднее клиентов на регион: {avg_per_region:.1f} 
            Общий объем продаж: {total_sales:,.0f} ₽ | Средние продажи на регион: {avg_sales_per_region:,.0f} ₽
            """
            self.stats_label.config(text=stats_text)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{str(e)}")

    def clear_table(self):
        """Очистка таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_pie_chart(self):
        """Показ круговой диаграммы"""
        try:
            # Получаем данные для графика
            query = """
            SELECT region, COUNT(*) as count 
            FROM clients 
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region 
            ORDER BY count DESC
            LIMIT 8
            """

            self.cursor.execute(query)
            data = self.cursor.fetchall()

            if not data:
                messagebox.showwarning("Нет данных", "Нет данных для построения графика")
                return

            # Создаем новое окно для графика
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Круговая диаграмма распределения по регионам")
            chart_window.geometry("800x600")

            # Создаем график
            regions = [row[0] for row in data]
            counts = [row[1] for row in data]

            fig, ax = plt.subplots(figsize=(10, 8))

            # Круговая диаграмма
            colors = plt.cm.Set3(range(len(regions)))
            wedges, texts, autotexts = ax.pie(
                counts,
                labels=regions,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                explode=[0.05] * len(regions)  # Немного отделяем куски
            )

            # Делаем проценты жирными
            for autotext in autotexts:
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')

            ax.set_title('ТОП-8 регионов по количеству клиентов', fontsize=16, fontweight='bold')
            ax.axis('equal')  # Чтобы круг был кругом

            plt.tight_layout()

            # Встраиваем в Tkinter
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Кнопка закрытия
            ttk.Button(chart_window, text="Закрыть",
                       command=chart_window.destroy).pack(pady=10)

            # Кнопка сохранения
            ttk.Button(chart_window, text="💾 Сохранить как PNG",
                       command=lambda: self.save_figure(fig, "pie_chart")).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")

    def show_bar_chart(self):
        """Показ столбчатой диаграммы"""
        try:
            # Получаем данные для графика
            query = """
            SELECT region, COUNT(*) as count, SUM(total_purchases) as sales
            FROM clients 
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region 
            ORDER BY count DESC
            LIMIT 10
            """

            self.cursor.execute(query)
            data = self.cursor.fetchall()

            if not data:
                messagebox.showwarning("Нет данных", "Нет данных для построения графика")
                return

            # Создаем новое окно для графика
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Столбчатая диаграмма по регионам")
            chart_window.geometry("900x600")

            # Создаем график
            regions = [row[0] for row in data]
            counts = [row[1] for row in data]
            sales = [row[2] / 1000 for row in data]  # В тысячах рублей

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

            # График 1: Количество клиентов
            bars1 = ax1.bar(regions, counts, color='skyblue', edgecolor='black', alpha=0.7)
            ax1.set_title('Количество клиентов по регионам (ТОП-10)', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Регион')
            ax1.set_ylabel('Количество клиентов')
            ax1.grid(True, alpha=0.3, axis='y')
            ax1.tick_params(axis='x', rotation=45)

            # Добавляем значения на столбцы
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                         f'{int(height)}', ha='center', va='bottom', fontsize=9)

            # График 2: Сумма покупок
            bars2 = ax2.bar(regions, sales, color='lightgreen', edgecolor='black', alpha=0.7)
            ax2.set_title('Сумма покупок по регионам (тыс. ₽)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Регион')
            ax2.set_ylabel('Сумма покупок (тыс. ₽)')
            ax2.grid(True, alpha=0.3, axis='y')
            ax2.tick_params(axis='x', rotation=45)

            # Добавляем значения на столбцы
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                         f'{height:,.0f}', ha='center', va='bottom', fontsize=9)

            plt.tight_layout()

            # Встраиваем в Tkinter
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Кнопки
            button_frame = ttk.Frame(chart_window)
            button_frame.pack(pady=10)

            ttk.Button(button_frame, text="Закрыть",
                       command=chart_window.destroy).pack(side=tk.LEFT, padx=5)

            ttk.Button(button_frame, text="💾 Сохранить график",
                       command=lambda: self.save_figure(fig, "bar_chart")).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")

    def save_figure(self, fig, filename_prefix):
        """Сохранение графика в файл"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"

            fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Сохранено", f"График сохранен в файл:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить график:\n{str(e)}")

    def export_to_csv(self):
        """Экспорт данных в CSV"""
        try:
            # Получаем данные для экспорта
            query = """
            SELECT 
                region,
                COUNT(*) as client_count,
                SUM(total_purchases) as total_sales,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 2) as percentage,
                ROUND(AVG(total_purchases), 2) as avg_purchase
            FROM clients
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region
            ORDER BY client_count DESC
            """

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                messagebox.showwarning("Нет данных", "Нет данных для экспорта")
                return

            # Создаем имя файла с timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"regional_analysis_{timestamp}.csv"

            # Экспортируем в файл
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')

                # Записываем заголовки
                writer.writerow(['Регион', 'Количество клиентов', 'Сумма покупок (₽)', 'Доля (%)', 'Средний чек (₽)'])

                # Записываем данные
                for region, count, sales, percentage, avg_purchase in results:
                    writer.writerow([region, count, sales, percentage, avg_purchase])

            messagebox.showinfo("Экспорт завершен",
                                f"✅ Данные успешно экспортированы в файл:\n{filename}\n"
                                f"Всего регионов: {len(results)}\n"
                                f"Формат: CSV с разделителем ';' (открывается в Excel)")

        except Exception as e:
            messagebox.showerror("Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")

    def show_help(self):
        """Показать справку по использованию"""
        help_text = """
        🎯 КАК ПОЛЬЗОВАТЬСЯ АЛГОРИТМОМ 1:

        1. ПРИ ЗАПУСКЕ программа автоматически:
           • Создает базу данных 'regional_analysis.db'
           • Генерирует демо-клиентов в 15 регионах России
           • Загружает данные в таблицу

        2. В ТАБЛИЦЕ вы видите:
           • Список регионов (отсортировано по количеству клиентов)
           • Количество клиентов в каждом регионе
           • Доля региона в процентах от общего числа клиентов
           • Сумма всех покупок клиентов региона
           • Сегмент (цветная иконка и текст):
             🔴 Высокий - более 15% клиентов
             🟡 Средний - от 5% до 15%
             🟢 Низкий - менее 5%

        3. КНОПКИ И ИХ ФУНКЦИИ:

           🔄 Обновить данные - перезагружает данные из базы
           📊 Круговая диаграмма - показывает ТОП-8 регионов на круговой диаграмме
           📈 Столбчатая диаграмма - показывает ТОП-10 регионов с двумя графиками:
              • Количество клиентов
              • Сумма покупок (в тыс. рублей)
           📄 Экспорт в CSV - сохраняет аналитику в CSV файл (открывается в Excel)
           🧹 Очистить таблицу - очищает таблицу (данные остаются в базе)
           ℹ️ Помощь - показывает эту инструкцию

        4. ВНИЗУ ОКНА отображается общая статистика:
           • Общее количество клиентов
           • Количество регионов
           • Среднее количество клиентов на регион
           • Общий объем продаж
           • Средние продажи на регион

        5. 💡 СОВЕТЫ:
           • Нажмите на заголовок столбца для сортировки (в некоторых версиях Python)
           • Экспортируйте данные для детального анализа в Excel
           • Используйте оба типа графиков для лучшего понимания данных

        6. ⚠️ ВНИМАНИЕ:
           • Все данные генерируются автоматически при первом запуске
           • Для реальных данных замените функцию create_demo_database
           • CSV файлы сохраняются в текущей папке с timestamp в имени
        """

        help_window = tk.Toplevel(self.root)
        help_window.title("Справка по использованию")
        help_window.geometry("700x600")

        text_widget = tk.Text(help_window, wrap="word", font=("Arial", 10))
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

        scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(help_window, text="Закрыть",
                   command=help_window.destroy).pack(pady=10)


# Запуск приложения
if __name__ == "__main__":
    # Указываем бэкенд для matplotlib (решает большинство проблем с графиками)
    import matplotlib

    matplotlib.use('TkAgg')  # Используем Tkinter-совместимый бэкенд

    root = tk.Tk()
    app = RegionalDistributionApp(root)
    root.mainloop()