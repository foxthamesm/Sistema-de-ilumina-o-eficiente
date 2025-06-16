import flet as ft
import asyncio
import httpx

API_URL = "https://api-de-ilumina-o.onrender.com/dados"  # Atualize com seu endpoint real da API

async def flet_main(page: ft.Page):
    page.title = "Gráfico em Tempo Real - Apresentação"
    page.theme_mode = ft.ThemeMode.DARK

    texto_erro = ft.Text("Não tenho acesso a API", visible=False, color=ft.Colors.RED, size=20)

    btn_leds_superior = ft.ElevatedButton("Gráfico LEDS superior", visible=False)
    btn_leds_inferior = ft.ElevatedButton("Gráfico LEDS inferior", visible=False)

    chart = ft.LineChart(
        expand=True,
        min_y=0,
        max_y=1023,
        data=[
            ft.LineChartData(point=[],  color=ft.Colors.RED),
            ft.LineChartData(point=[],  color=ft.Colors.BLUE_GREY),
            ft.LineChartData(point=[],  color=ft.Colors.GREEN),
        ],
        visible=False,
    )

    page.add(texto_erro, btn_leds_superior, btn_leds_inferior, chart)

    async def testar_api():
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(API_URL, timeout=3)
                if r.status_code == 200:
                    texto_erro.visible = False
                    btn_leds_superior.visible = True
                    btn_leds_inferior.visible = True
                    chart.visible = True
                    page.update()
                    return True
                else:
                    raise Exception("Status code diferente de 200")
            except Exception:
                texto_erro.visible = True
                btn_leds_superior.visible = False
                btn_leds_inferior.visible = False
                chart.visible = False
                page.update()
                return False

    async def atualizar_chart_periodicamente():
        if not await testar_api():
            return  # Não faz nada se API não acessível

        async with httpx.AsyncClient() as client:
            while True:
                try:
                    r = await client.get(API_URL)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("tempo"):
                            chart.data[0].points = [
                                ft.LineChartDataPoint(x, y) for x, y in zip(data["tempo"], data["ldr_a"])
                            ]
                            chart.data[1].points = [
                                ft.LineChartDataPoint(x, y) for x, y in zip(data["tempo"], data["ldr_b"])
                            ]
                            chart.data[2].points = [
                                ft.LineChartDataPoint(x, y) for x, y in zip(data["tempo"], data["intensidade"])
                            ]
                            page.update()
                except Exception as e:
                    print("Erro ao buscar dados da API:", e)
                await asyncio.sleep(0.5)

    asyncio.create_task(atualizar_chart_periodicamente())

if __name__ == "__main__":
    ft.app(target=flet_main, port=8501, view=None)
import flet as ft
import asyncio
import httpx

API_URL = "https://SEU-ENDERECO-DA-API/render-url/dados"  # Atualize com seu endpoint real da API

async def flet_main(page: ft.Page):
    page.title = "Gráfico em Tempo Real - Apresentação"
    page.theme_mode = ft.ThemeMode.DARK

    texto_erro = ft.Text("Não tenho acesso a API", visible=False, color=ft.Colors.RED, size=20)

    btn_leds_superior = ft.ElevatedButton("Gráfico LEDS superior", visible=False)
    btn_leds_inferior = ft.ElevatedButton("Gráfico LEDS inferior", visible=False)

    chart = ft.LineChart(
        expand=True,
        min_y=0,
        max_y=1023,
        data=[
            ft.LineChartData(point=[], stroke_color=ft.Colors.RED, name="LDR A"),
            ft.LineChartData(point=[], stroke_color=ft.Colors.BLUE, name="LDR B"),
            ft.LineChartData(point=[], stroke_color=ft.Colors.GREEN, name="Intensidade"),
        ],
        visible=False,
    )

    page.add(texto_erro, btn_leds_superior, btn_leds_inferior, chart)

    async def testar_api():
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(API_URL, timeout=3)
                if r.status_code == 200:
                    texto_erro.visible = False
                    btn_leds_superior.visible = True
                    btn_leds_inferior.visible = True
                    chart.visible = True
                    page.update()
                    return True
                else:
                    raise Exception("Status code diferente de 200")
            except Exception:
                texto_erro.visible = True
                btn_leds_superior.visible = False
                btn_leds_inferior.visible = False
                chart.visible = False
                page.update()
                return False

    async def atualizar_chart_periodicamente():
        if not await testar_api():
            return  # Não faz nada se API não acessível

        async with httpx.AsyncClient() as client:
            while True:
                try:
                    r = await client.get(API_URL)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("tempo"):
                            chart.data[0].points = [
                                ft.LineChartDataPoint(x, y) for x, y in zip(data["tempo"], data["ldr_a"])
                            ]
                            chart.data[1].points = [
                                ft.LineChartDataPoint(x, y) for x, y in zip(data["tempo"], data["ldr_b"])
                            ]
                            chart.data[2].points = [
                                ft.LineChartDataPoint(x, y) for x, y in zip(data["tempo"], data["intensidade"])
                            ]
                            page.update()
                except Exception as e:
                    print("Erro ao buscar dados da API:", e)
                await asyncio.sleep(0.5)

    asyncio.create_task(atualizar_chart_periodicamente())

if __name__ == "__main__":
    ft.app(target=flet_main, port=8501, view=None)
