import flet as ft
from fastapi import FastAPI
from pydantic import BaseModel
import threading
import asyncio

dados_tempo = []
dados_ldr_a = []
dados_ldr_b = []
dados_intensidade = []

MAX_PONTOS = 1000

app_api = FastAPI()

class Dados(BaseModel):
    tempo: float
    ldr_a: int
    ldr_b: int
    intensidade: int

def adicionar_dado(lista, valor):
    lista.append(valor)
    if len(lista) > MAX_PONTOS:
        lista.pop(0)

@app_api.post("/enviar_dados")
async def receber_dados(dados: Dados):
    adicionar_dado(dados_tempo, dados.tempo)
    adicionar_dado(dados_ldr_a, dados.ldr_a)
    adicionar_dado(dados_ldr_b, dados.ldr_b)
    adicionar_dado(dados_intensidade, dados.intensidade)
    return {"mensagem": "Dados recebidos com sucesso."}

async def flet_main(page: ft.Page):
    page.title = "Gráfico em Tempo Real - Apresentação"
    page.theme_mode = ft.ThemeMode.DARK

    chart = ft.LineChart(
        expand=True,
        min_y=0,
        max_y=1023,
        series=[
            ft.LineChartSeries(data_points=[], stroke_color=ft.colors.RED, name="LDR A"),
            ft.LineChartSeries(data_points=[], stroke_color=ft.colors.BLUE, name="LDR B"),
            ft.LineChartSeries(data_points=[], stroke_color=ft.colors.GREEN, name="Intensidade"),
        ],
    )

    page.add(chart)

    async def atualizar_chart():
        while True:
            if dados_tempo:
                chart.series[0].data_points = [
                    ft.LineChartDataPoint(x, y) for x, y in zip(dados_tempo, dados_ldr_a)
                ]
                chart.series[1].data_points = [
                    ft.LineChartDataPoint(x, y) for x, y in zip(dados_tempo, dados_ldr_b)
                ]
                chart.series[2].data_points = [
                    ft.LineChartDataPoint(x, y) for x, y in zip(dados_tempo, dados_intensidade)
                ]
                page.update()
            await asyncio.sleep(0.5)

    asyncio.create_task(atualizar_chart())

def main():
    import uvicorn
    threading.Thread(target=lambda: uvicorn.run(app_api, host="0.0.0.0", port=8000), daemon=True).start()
    ft.app(target=flet_main, port=8501, view=None)

if __name__ == "__main__":
    main()
