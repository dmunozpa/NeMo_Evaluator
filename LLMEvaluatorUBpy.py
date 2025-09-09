import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import threading
import random
import string
from datetime import datetime
from nemo_microservices import NeMoMicroservices

class NeMoEvaluatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeMo Evaluator - Interfaz Gráfica")
        self.root.geometry("1200x900")
        
        # Variables para almacenar configuraciones
        self.prompts_folder = tk.StringVar()
        self.selected_model = tk.StringVar(value="meta/llama-3.1-8b-instruct")
        
        # Variables de configuración general
        self.base_url_microservices = tk.StringVar(value="http://localhost:7331")
        self.nvidia_api_key = tk.StringVar(value="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")
        self.base_url_api = tk.StringVar(value="https://integrate.api.nvidia.com/v1")
        self.pattern_score = tk.StringVar(value="METRIC_VALUE: (\\\\d)")
        
        # Variables de parámetros
        self.params_vars = {}
        self.extra_vars = {}
        
        # Variables de métricas
        self.metrics_vars = {}
        
        # Variables de datos
        self.data_id = tk.StringVar()
        self.data_query = tk.StringVar()
        self.data_response = tk.StringVar()
        self.data_truth = tk.StringVar()
        
        self.create_widgets()
        self.generate_new_id()
        
    def create_widgets(self):
        # Crear notebook para organizar en pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Configuración General
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuración General")
        self.create_general_config(config_frame)
        
        # Pestaña 2: Modelo y Parámetros
        model_frame = ttk.Frame(notebook)
        notebook.add(model_frame, text="Modelo y Parámetros")
        self.create_model_params(model_frame)
        
        # Pestaña 3: Métricas
        metrics_frame = ttk.Frame(notebook)
        notebook.add(metrics_frame, text="Métricas")
        self.create_metrics_config(metrics_frame)
        
        # Pestaña 4: Datos y Ejecución
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="Datos y Ejecución")
        self.create_data_execution(data_frame)
        
    def create_general_config(self, parent):
        # Marco principal con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configuración General
        config_group = ttk.LabelFrame(scrollable_frame, text="Configuración General", padding=10)
        config_group.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(config_group, text="Base URL Microservicios:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(config_group, textvariable=self.base_url_microservices, width=50).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_group, text="API Key NVIDIA:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(config_group, textvariable=self.nvidia_api_key, width=50, show="*").grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_group, text="Base URL API:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(config_group, textvariable=self.base_url_api, width=50).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_group, text="Patrón de Resultados:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(config_group, textvariable=self.pattern_score, width=50).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_model_params(self, parent):
        # Marco principal con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Selección de carpeta de prompts
        prompts_group = ttk.LabelFrame(scrollable_frame, text="Configuración de Prompts", padding=10)
        prompts_group.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(prompts_group, text="Carpeta de Prompts:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(prompts_group, textvariable=self.prompts_folder, width=40).grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(prompts_group, text="Buscar", command=self.select_prompts_folder).grid(row=0, column=2, padx=5)
        
        # Selección de modelo
        model_group = ttk.LabelFrame(scrollable_frame, text="Selección de Modelo", padding=10)
        model_group.pack(fill=tk.X, padx=10, pady=5)
        
        models = [
            "meta/llama-3.1-8b-instruct",
            "deepseek-ai/deepseek-v3.1",
            "meta/llama-3.3-70b-instruct",
            "nvidia/llama-3.1-nemoguard-8b-content-safety"
        ]
        
        ttk.Label(model_group, text="Modelo:").grid(row=0, column=0, sticky=tk.W)
        model_combo = ttk.Combobox(model_group, textvariable=self.selected_model, values=models, width=50, state="readonly")
        model_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Parámetros principales
        params_group = ttk.LabelFrame(scrollable_frame, text="Parámetros Principales", padding=10)
        params_group.pack(fill=tk.X, padx=10, pady=5)
        
        params_config = [
            ("parallelims", 20, "int"),
            ("temperature", 0.1, "float"),
            ("top_p", 0.0, "float"),
            ("max_tokens", 16, "int"),
            ("max_retries", 1, "int"),
            ("request_timeout", 10, "int")
        ]
        
        for i, (param, default, param_type) in enumerate(params_config):
            var_check = tk.BooleanVar()
            var_value = tk.StringVar(value=str(default))
            self.params_vars[param] = {"enabled": var_check, "value": var_value, "type": param_type}
            
            ttk.Checkbutton(params_group, text=param, variable=var_check).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(params_group, textvariable=var_value, width=20)
            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=2)
        
        # Parámetros extras
        extra_group = ttk.LabelFrame(scrollable_frame, text="Parámetros Extras", padding=10)
        extra_group.pack(fill=tk.X, padx=10, pady=5)
        
        # batch_size
        var_check = tk.BooleanVar()
        var_value = tk.StringVar(value="8")
        self.extra_vars["batch_size"] = {"enabled": var_check, "value": var_value, "type": "int"}
        ttk.Checkbutton(extra_group, text="batch_size", variable=var_check).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(extra_group, textvariable=var_value, width=20).grid(row=0, column=1, sticky=tk.W, padx=10, pady=2)
        
        # use_gredy
        var_check = tk.BooleanVar()
        var_value = tk.StringVar(value="True")
        self.extra_vars["use_gredy"] = {"enabled": var_check, "value": var_value, "type": "bool"}
        ttk.Checkbutton(extra_group, text="use_gredy", variable=var_check).grid(row=1, column=0, sticky=tk.W, pady=2)
        combo = ttk.Combobox(extra_group, textvariable=var_value, values=["True", "False"], width=17, state="readonly")
        combo.grid(row=1, column=1, sticky=tk.W, padx=10, pady=2)
        
        # top_k
        var_check = tk.BooleanVar()
        var_value = tk.StringVar(value="1")
        self.extra_vars["top_k"] = {"enabled": var_check, "value": var_value, "type": "int"}
        ttk.Checkbutton(extra_group, text="top_k", variable=var_check).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(extra_group, textvariable=var_value, width=20).grid(row=2, column=1, sticky=tk.W, padx=10, pady=2)
        
        # limit_samples
        var_check = tk.BooleanVar()
        var_value = tk.StringVar(value="100")
        self.extra_vars["limit_samples"] = {"enabled": var_check, "value": var_value, "type": "int"}
        ttk.Checkbutton(extra_group, text="limit_samples", variable=var_check).grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(extra_group, textvariable=var_value, width=20).grid(row=3, column=1, sticky=tk.W, padx=10, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_metrics_config(self, parent):
        # Marco principal con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Métricas
        metrics_group = ttk.LabelFrame(scrollable_frame, text="Selección de Métricas", padding=10)
        metrics_group.pack(fill=tk.X, padx=10, pady=5)
        
        metrics_list = [
            "toxicidad", "tonalidad", "sesgo", "claridad", "calidad_razonamiento",
            "coherencia", "helpfulness", "sentimiento", "instruccion_following", "prompt_multiple"
        ]
        
        # Crear checkbuttons para métricas en 2 columnas
        for i, metric in enumerate(metrics_list):
            var = tk.BooleanVar()
            self.metrics_vars[metric] = var
            row = i // 2
            col = i % 2
            ttk.Checkbutton(metrics_group, text=metric, variable=var).grid(row=row, column=col, sticky=tk.W, padx=20, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_data_execution(self, parent):
        # Marco principal con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Datos de entrada
        data_group = ttk.LabelFrame(scrollable_frame, text="Datos de Evaluación", padding=10)
        data_group.pack(fill=tk.X, padx=10, pady=5)
        
        # ID
        id_frame = ttk.Frame(data_group)
        id_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E, pady=2)
        ttk.Label(id_frame, text="ID:").pack(side=tk.LEFT)
        ttk.Entry(id_frame, textvariable=self.data_id, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(id_frame, text="Generar Nuevo", command=self.generate_new_id).pack(side=tk.LEFT, padx=10)
        
        # Consulta
        ttk.Label(data_group, text="Consulta:").grid(row=1, column=0, sticky=tk.W+tk.N, pady=2)
        query_text = tk.Text(data_group, height=3, width=80)
        query_text.grid(row=1, column=1, sticky=tk.W+tk.E, pady=2)
        query_text.bind('<KeyRelease>', lambda e: self.data_query.set(query_text.get("1.0", tk.END)))
        
        # Respuesta
        ttk.Label(data_group, text="Respuesta:").grid(row=2, column=0, sticky=tk.W+tk.N, pady=2)
        response_text = tk.Text(data_group, height=4, width=80)
        response_text.grid(row=2, column=1, sticky=tk.W+tk.E, pady=2)
        response_text.bind('<KeyRelease>', lambda e: self.data_response.set(response_text.get("1.0", tk.END)))
        
        # Verdad
        ttk.Label(data_group, text="Verdad (Opcional):").grid(row=3, column=0, sticky=tk.W+tk.N, pady=2)
        truth_text = tk.Text(data_group, height=3, width=80)
        truth_text.grid(row=3, column=1, sticky=tk.W+tk.E, pady=2)
        truth_text.bind('<KeyRelease>', lambda e: self.data_truth.set(truth_text.get("1.0", tk.END)))
        
        # Configurar expansión de columnas
        data_group.columnconfigure(1, weight=1)
        
        # Botones de acción
        buttons_group = ttk.LabelFrame(scrollable_frame, text="Acciones", padding=10)
        buttons_group.pack(fill=tk.X, padx=10, pady=5)
        
        button_frame = ttk.Frame(buttons_group)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Ejecutar Evaluación", command=self.run_evaluation).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Limpiar Datos", command=self.clear_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT, padx=10)
        
        # Log de ejecución
        log_group = ttk.LabelFrame(scrollable_frame, text="Log de Ejecución", padding=10)
        log_group.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_group, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def select_prompts_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta de prompts")
        if folder:
            self.prompts_folder.set(folder)
            
    def generate_new_id(self):
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        self.data_id.set(new_id)
        
    def clear_data(self):
        self.data_query.set("")
        self.data_response.set("")
        self.data_truth.set("")
        self.generate_new_id()
        
    def log_message(self, message):
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def validate_inputs(self):
        # Validar campos obligatorios
        if not self.prompts_folder.get():
            messagebox.showerror("Error", "Debe seleccionar una carpeta de prompts")
            return False
            
        if not self.data_query.get().strip():
            messagebox.showerror("Error", "Debe ingresar una consulta")
            return False
            
        if not self.data_response.get().strip():
            messagebox.showerror("Error", "Debe ingresar una respuesta")
            return False
            
        # Validar que al menos una métrica esté seleccionada
        selected_metrics = [metric for metric, var in self.metrics_vars.items() if var.get()]
        if not selected_metrics:
            messagebox.showerror("Error", "Debe seleccionar al menos una métrica")
            return False
            
        return True
        
    def leer_prompt(self, name):
        try:
            prompt_path = os.path.join(self.prompts_folder.get(), f"{name}.prompt")
            with open(prompt_path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.log_message(f"Error leyendo prompt {name}: {str(e)}")
            return ""
            
    def build_config(self, project_name, base_url, model_id, api_key, lista_metricas, rows, pattern_score):
        def make_metric_config(metrica):
            return {
                f"{metrica}_{model_id}": {
                    "type": "llm-judge",
                    "params": {
                        "model": {
                            "api_endpoint": {
                                "url": base_url,
                                "model_id": model_id,
                                "api_key": api_key,
                            }
                        },
                        "extra": self.get_extra_params(),
                        "template": {
                            "messages": [
                                {
                                    "role": "system",
                                    "content": self.leer_prompt("system"),
                                    "temperature": 0,
                                    "top_p": 0.9,
                                },
                                {
                                    "role": "user",
                                    "content": self.leer_prompt(metrica),
                                },
                            ]
                        },
                        "scores": {
                            f"{metrica}_score": {
                                "type": "int",
                                "parser": {
                                    "type": "regex",
                                    "pattern": pattern_score,
                                },
                            }
                        },
                    },
                }
            }

        tasks = {}
        for metrica in lista_metricas:
            tasks[f"Task_{metrica}"] = {
                "type": "data",
                "metrics": make_metric_config(metrica),
            }

        config = {
            "project": project_name,
            "type": "custom",
            "timeout": None,
            "params": self.get_params(),
            "tasks": tasks,
        }

        target = {
            "type": "rows",
            "rows": rows,
        }

        return config, target
        
    def get_params(self):
        params = {}
        for param_name, param_data in self.params_vars.items():
            if param_data["enabled"].get():
                try:
                    value = param_data["value"].get()
                    if param_data["type"] == "int":
                        params[param_name] = int(value)
                    elif param_data["type"] == "float":
                        params[param_name] = float(value)
                except ValueError:
                    self.log_message(f"Error: Valor inválido para {param_name}: {value}")
        return params
        
    def get_extra_params(self):
        extra = {}
        for param_name, param_data in self.extra_vars.items():
            if param_data["enabled"].get():
                try:
                    value = param_data["value"].get()
                    if param_data["type"] == "int":
                        extra[param_name] = int(value)
                    elif param_data["type"] == "bool":
                        extra[param_name] = value == "True"
                except ValueError:
                    self.log_message(f"Error: Valor inválido para {param_name}: {value}")
        return extra
        
    def run_evaluation(self):
        if not self.validate_inputs():
            return
            
        # Ejecutar en un hilo separado para no bloquear la GUI
        thread = threading.Thread(target=self._execute_evaluation)
        thread.daemon = True
        thread.start()
        
    def _execute_evaluation(self):
        try:
            self.log_message("Iniciando evaluación...")
            
            # Configurar variables de entorno
            os.environ["NVIDIA_API_KEY"] = self.nvidia_api_key.get()
            
            # Inicializar cliente
            client = NeMoMicroservices(base_url=self.base_url_microservices.get())
            self.log_message("Cliente NeMo inicializado")
            
            # Obtener métricas seleccionadas
            selected_metrics = [metric for metric, var in self.metrics_vars.items() if var.get()]
            self.log_message(f"Métricas seleccionadas: {', '.join(selected_metrics)}")
            
            # Preparar datos
            rows = [{
                "id": self.data_id.get(),
                "Consulta": self.data_query.get().strip(),
                "Respuesta": self.data_response.get().strip(),
            }]
            
            if self.data_truth.get().strip():
                rows[0]["Verdad"] = self.data_truth.get().strip()
            
            # Construir configuración
            config, target = self.build_config(
                project_name="demo_oxigeno",
                base_url=self.base_url_api.get(),
                model_id=self.selected_model.get(),
                api_key=self.nvidia_api_key.get(),
                lista_metricas=selected_metrics,
                rows=rows,
                pattern_score=self.pattern_score.get(),
            )
            
            self.log_message(f"Ejecutando evaluación con modelo: {self.selected_model.get()}")
            
            # Ejecutar evaluación
            start_time = datetime.now()
            response = client.evaluation.live(config=config, target=target)
            latencia = datetime.now() - start_time
            
            # Mostrar resultados
            self.log_message(f"Evaluación completada!")
            self.log_message(f"Latencia: {latencia.total_seconds():.2f} segundos")
            self.log_message(f"Status: {response.status}")
            self.log_message(f"Status Details: {response.status_details}")
            
            # Guardar resultados
            result_id = response.result.id
            
            # Guardar logs
            with open(f"results_{result_id}.json", "w+", encoding="utf-8") as jf:
                json.dump(response.logs, jf, ensure_ascii=False, indent=4)
            self.log_message(f"Logs guardados en: results_{result_id}.json")
            
            # Función para serializar objetos
            def custom_serializer(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                elif hasattr(obj, "__dict__"):
                    return {key: custom_serializer(value) for key, value in obj.__dict__.items()}
                elif isinstance(obj, dict):
                    return {key: custom_serializer(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [custom_serializer(item) for item in obj]
                else:
                    return obj
            
            # Guardar respuesta
            json_output = json.dumps(response.result, default=custom_serializer, indent=2)
            with open(f"response_{result_id}.json", "w+", encoding="utf-8") as f:
                f.write(json_output)
            self.log_message(f"Respuesta guardada en: response_{result_id}.json")
            
            messagebox.showinfo("Éxito", f"Evaluación completada exitosamente!\nID: {result_id}")
            
        except Exception as e:
            error_msg = f"Error durante la evaluación: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)

def main():
    root = tk.Tk()
    app = NeMoEvaluatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
