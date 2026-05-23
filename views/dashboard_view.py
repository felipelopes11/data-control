import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

IPIRANGA_AMARELO = "#FFD100"
IPIRANGA_AZUL = "#003B8D"
IPIRANGA_AZUL_CLARO = "#0066CC"
IPIRANGA_LARANJA = "#F47920"
IPIRANGA_BRANCO = "#FFFFFF"
IPIRANGA_CINZA_FUNDO = "#F0F2F6"

CORES_GRAFICOS = [
    "#003B8D", "#FFD100", "#F47920", "#0066CC",
    "#E8A800", "#00529B", "#FF9F43", "#2E86DE",
    "#F39C12", "#1E3A5F"
]


def _aplicar_css_personalizado():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #003B8D 0%, #001F4D 100%);
        }
        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMultiSelect label {
            color: #FFD100 !important;
            font-weight: 600;
        }

        .kpi-card {
            background: linear-gradient(135deg, #003B8D 0%, #0066CC 100%);
            border-radius: 12px;
            padding: 20px 18px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 59, 141, 0.18);
            border-left: 5px solid #FFD100;
            transition: transform 0.2s ease;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
        }
        .kpi-label {
            color: #B8D4F0;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .kpi-valor {
            color: #FFFFFF;
            font-size: 1.65rem;
            font-weight: 700;
            line-height: 1.2;
        }
        .kpi-detalhe {
            color: #FFD100;
            font-size: 0.78rem;
            margin-top: 4px;
            font-weight: 500;
        }

        .header-banner {
            background: linear-gradient(135deg, #003B8D 0%, #001F4D 60%, #0066CC 100%);
            border-radius: 14px;
            padding: 28px 36px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 6px 24px rgba(0, 59, 141, 0.22);
            border-bottom: 4px solid #FFD100;
        }
        .header-titulo {
            color: #FFFFFF;
            font-size: 1.9rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0.5px;
        }
        .header-subtitulo {
            color: #B8D4F0;
            font-size: 0.95rem;
            margin: 4px 0 0 0;
        }
        .header-badge {
            background: #FFD100;
            color: #003B8D;
            font-weight: 800;
            font-size: 0.75rem;
            padding: 6px 16px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .secao-titulo {
            color: #003B8D;
            font-size: 1.15rem;
            font-weight: 700;
            margin: 28px 0 12px 0;
            padding-bottom: 6px;
            border-bottom: 3px solid #FFD100;
            display: inline-block;
        }

        .footer-info {
            text-align: center;
            color: #8899AA;
            font-size: 0.78rem;
            padding: 20px 0 8px 0;
            border-top: 1px solid #E0E5EC;
            margin-top: 32px;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 24px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)


class DashboardView:
    def render_header(self):
        st.set_page_config(
            page_title="Auto Posto Santa Cruz – Painel de Vendas",
            page_icon="⛽",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        _aplicar_css_personalizado()

        st.markdown("""
        <div class="header-banner">
            <div>
                <p class="header-titulo">⛽ Auto Posto Santa Cruz</p>
                <p class="header-subtitulo">Painel de Acompanhamento de Vendas e Abastecimentos</p>
            </div>
            <div class="header-badge">Rede Ipiranga</div>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self, frentistas, combustiveis):
        with st.sidebar:
            st.markdown("## ⛽ Filtros")
            st.markdown("---")
            frentista_selecionado = st.selectbox(
                "Frentista",
                options=frentistas,
                index=0
            )
            combustiveis_selecionados = st.multiselect(
                "Combustíveis",
                options=combustiveis,
                default=combustiveis
            )
            st.markdown("---")
            st.markdown(
                "<p style='text-align:center;font-size:0.72rem;color:#B8D4F0;'>"
                "Auto Posto Santa Cruz<br>Rede Ipiranga</p>",
                unsafe_allow_html=True
            )

        return frentista_selecionado, combustiveis_selecionados

    def render_error(self, message):
        st.error(message)

    def render_warning(self, message):
        st.warning(message)

    def _render_kpis(self, dados):
        total_litros = dados["Litros"].sum()
        total_valor = dados["Valor_Total"].sum()
        total_abastecimentos = len(dados)
        ticket_medio = total_valor / total_abastecimentos if total_abastecimentos else 0

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Abastecimentos</div>
                <div class="kpi-valor">{total_abastecimentos:,.0f}</div>
                <div class="kpi-detalhe">registros filtrados</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Litros Vendidos</div>
                <div class="kpi-valor">{total_litros:,.1f}</div>
                <div class="kpi-detalhe">litros no período</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Faturamento</div>
                <div class="kpi-valor">R$ {total_valor:,.2f}</div>
                <div class="kpi-detalhe">valor arrecadado</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Ticket Médio</div>
                <div class="kpi-valor">R$ {ticket_medio:,.2f}</div>
                <div class="kpi-detalhe">por abastecimento</div>
            </div>""", unsafe_allow_html=True)

    def _layout_padrao(self, fig, altura=420, mostrar_legenda=True):
        fig.update_layout(
            template="plotly_white",
            font=dict(family="Segoe UI, sans-serif", size=12, color="#333"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=altura,
            margin=dict(l=40, r=20, t=50, b=100),
            showlegend=mostrar_legenda,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.35,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            title_font=dict(size=15, color=IPIRANGA_AZUL, family="Segoe UI, sans-serif"),
            xaxis_tickangle=-20,
        )
        return fig

    def render_dashboard(self, dados_filtrados):
        self._render_kpis(dados_filtrados)

        st.markdown("<br>", unsafe_allow_html=True)

        tab_combustivel, tab_frentista, tab_temporal, tab_dados = st.tabs([
            "🛢️ Por Combustível",
            "👷 Por Frentista",
            "📈 Evolução Temporal",
            "📋 Dados Detalhados"
        ])

        with tab_combustivel:
            st.markdown('<p class="secao-titulo">Análise por Tipo de Combustível</p>',
                        unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                litros_comb = dados_filtrados.groupby("Combustivel")["Litros"].sum().reset_index()
                litros_comb = litros_comb.sort_values("Litros", ascending=False)
                fig_litros = px.bar(
                    litros_comb, x="Combustivel", y="Litros",
                    color="Combustivel",
                    color_discrete_sequence=CORES_GRAFICOS,
                    title="Litros Vendidos por Combustível",
                    text_auto=".2s"
                )
                fig_litros.update_traces(
                    textposition="outside",
                    marker_line_width=0,
                )
                fig_litros = self._layout_padrao(fig_litros, mostrar_legenda=False)
                st.plotly_chart(fig_litros, width="stretch")

            with col2:
                valor_comb = dados_filtrados.groupby("Combustivel")["Valor_Total"].sum().reset_index()
                fig_pizza = px.pie(
                    valor_comb, names="Combustivel", values="Valor_Total",
                    color_discrete_sequence=CORES_GRAFICOS,
                    title="Participação no Faturamento",
                    hole=0.45
                )
                fig_pizza.update_traces(
                    textinfo="percent+label",
                    textfont_size=11,
                    marker=dict(line=dict(color="#FFFFFF", width=2))
                )
                fig_pizza = self._layout_padrao(fig_pizza)
                st.plotly_chart(fig_pizza, width="stretch")

            st.markdown('<p class="secao-titulo">Frequência de Abastecimentos</p>',
                        unsafe_allow_html=True)
            transacoes = dados_filtrados["Combustivel"].value_counts().reset_index()
            transacoes.columns = ["Combustivel", "Quantidade"]
            transacoes = transacoes.sort_values("Quantidade", ascending=True)
            fig_freq = px.bar(
                transacoes, x="Quantidade", y="Combustivel",
                orientation="h",
                color="Combustivel",
                color_discrete_sequence=CORES_GRAFICOS,
                title="Quantidade de Abastecimentos por Combustível",
                text_auto=True
            )
            fig_freq.update_traces(
                textposition="outside",
                marker_line_width=0,
            )
            fig_freq = self._layout_padrao(fig_freq, altura=350, mostrar_legenda=False)
            st.plotly_chart(fig_freq, width="stretch")

        with tab_frentista:
            st.markdown('<p class="secao-titulo">Desempenho por Frentista</p>',
                        unsafe_allow_html=True)

            col_a, col_b = st.columns(2)

            with col_a:
                vendas_fr = dados_filtrados.groupby("Frentista")["Valor_Total"].sum().reset_index()
                vendas_fr = vendas_fr.sort_values("Valor_Total", ascending=True)
                fig_fr = px.bar(
                    vendas_fr, x="Valor_Total", y="Frentista",
                    orientation="h",
                    color_discrete_sequence=[IPIRANGA_AZUL],
                    title="Faturamento por Frentista (R$)",
                    text_auto=".2s"
                )
                fig_fr.update_traces(
                    textposition="outside",
                    marker_line_width=0,
                )
                fig_fr = self._layout_padrao(fig_fr, altura=max(350, len(vendas_fr) * 38))
                st.plotly_chart(fig_fr, width="stretch")

            with col_b:
                litros_fr = dados_filtrados.groupby("Frentista")["Litros"].sum().reset_index()
                litros_fr = litros_fr.sort_values("Litros", ascending=True)
                fig_lr = px.bar(
                    litros_fr, x="Litros", y="Frentista",
                    orientation="h",
                    color_discrete_sequence=[IPIRANGA_LARANJA],
                    title="Litros Abastecidos por Frentista",
                    text_auto=".2s"
                )
                fig_lr.update_traces(
                    textposition="outside",
                    marker_line_width=0,
                )
                fig_lr = self._layout_padrao(fig_lr, altura=max(350, len(litros_fr) * 38))
                st.plotly_chart(fig_lr, width="stretch")

        with tab_temporal:
            st.markdown('<p class="secao-titulo">Evolução ao Longo do Tempo</p>',
                        unsafe_allow_html=True)

            vendas_tempo = dados_filtrados.groupby("Data").agg(
                Valor_Total=("Valor_Total", "sum"),
                Litros=("Litros", "sum"),
                Abastecimentos=("Valor_Total", "count")
            ).reset_index().sort_values("Data")

            fig_tempo = go.Figure()
            fig_tempo.add_trace(go.Scatter(
                x=vendas_tempo["Data"], y=vendas_tempo["Valor_Total"],
                mode="lines+markers",
                name="Faturamento (R$)",
                line=dict(color=IPIRANGA_AZUL, width=2.5),
                marker=dict(size=5),
                fill="tozeroy",
                fillcolor="rgba(0,59,141,0.08)"
            ))
            fig_tempo.update_layout(
                title="Faturamento Diário (R$)",
                xaxis_title="Data",
                yaxis_title="Valor (R$)",
            )
            fig_tempo = self._layout_padrao(fig_tempo, altura=400)
            st.plotly_chart(fig_tempo, width="stretch")

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                fig_litros_t = go.Figure()
                fig_litros_t.add_trace(go.Scatter(
                    x=vendas_tempo["Data"], y=vendas_tempo["Litros"],
                    mode="lines+markers",
                    name="Litros",
                    line=dict(color=IPIRANGA_LARANJA, width=2),
                    marker=dict(size=4),
                    fill="tozeroy",
                    fillcolor="rgba(244,121,32,0.08)"
                ))
                fig_litros_t.update_layout(title="Litros Vendidos por Dia")
                fig_litros_t = self._layout_padrao(fig_litros_t, altura=340)
                st.plotly_chart(fig_litros_t, width="stretch")

            with col_t2:
                fig_abt = go.Figure()
                fig_abt.add_trace(go.Bar(
                    x=vendas_tempo["Data"], y=vendas_tempo["Abastecimentos"],
                    name="Abastecimentos",
                    marker_color=IPIRANGA_AMARELO,
                    marker_line_width=0,
                ))
                fig_abt.update_layout(title="Abastecimentos por Dia")
                fig_abt = self._layout_padrao(fig_abt, altura=340)
                st.plotly_chart(fig_abt, width="stretch")

        with tab_dados:
            st.markdown('<p class="secao-titulo">Dados Filtrados</p>',
                        unsafe_allow_html=True)
            st.markdown(f"**{len(dados_filtrados):,}** registros encontrados com os filtros selecionados.")
            st.dataframe(
                dados_filtrados,
                width="stretch",
                height=500,
            )

        st.markdown(
            '<div class="footer-info">'
            '⛽ Auto Posto Santa Cruz · Rede Ipiranga · '
            'Dashboard desenvolvido com Streamlit, Plotly e Pandas'
            '</div>',
            unsafe_allow_html=True
        )
