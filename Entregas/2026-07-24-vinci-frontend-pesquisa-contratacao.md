# Pesquisa de Contratação: Vinci (Desenvolvedor Frontend & UI/UX)

- **Data:** 2026-07-24
- **Papel:** Desenvolvedor Frontend e UI/UX especialista em painéis interativos e design systems para Web.
- **Objetivo:** Adicionar ao time um especialista capaz de realizar refinamentos estéticos, dinâmicas de interface responsiva e lógica de estado no navegador (como acumuladores de histórico e visualizações compactas de estoque).

---

## 1. Competências Centrais

A melhor versão deste papel deve:
* **Domínio de CSS Moderno e Responsivo:** Construir layouts compactos, adaptáveis (usando CSS Grid e Flexbox) e visualmente ricos (respeitando paletas refinadas e eliminando excesso de espaço em branco).
* **Experiência em Dashboards Comerciais:** Entender como dados numéricos complexos (vendas diárias, metas de break-even e saldos de insumo) devem ser apresentados de maneira legível em telas de diferentes tamanhos.
* **Manipulação de Estado Local (LocalStorage):** Saber projetar estruturas de dados robustas para persistência no navegador, como histórico de transações com controle de data, garantindo migração suave de esquemas antigos.
* **Foco em UX e Micro-Interações:** Criar checklists dinâmicos com ocultação inteligente de tarefas concluídas, estados hover e transições suaves que deixam a interface responsiva e viva.

## 2. Anti-Padrões a Evitar

* **Uso Inadequado de Frameworks Pesados:** Evitar tentar instalar dependências desnecessárias ou reconstruir páginas simples de arquivo único em frameworks robustos, a menos que solicitado.
* **Desperdício de Espaço Vertical (Scrolling excessivo):** Não agrupar dados em listas verticais extensas quando um grid compacto (ex: 8 por linha) é muito mais visual e eficiente.
* **Falta de Fallback ou Migração de Dados:** Reescrever ou apagar a chave de `localStorage` do usuário sem migrar o formato de dados anterior, causando perda de informações operacionais do dia.

## 3. Entregáveis de Vinci

* **HTML/CSS Polidos:** Códigos limpos com variáveis e tokens de cores integrados no design system existente.
* **Lógica JS de Histórico Temporal:** Implementação de acumulador de vendas agrupado por data, permitindo consultas históricas retroativas e cálculo de progresso mensal acumulado.
* **Layouts de Grid Compactos:** Refatoração de listas de saldo e insumos para blocos pequenos com botões de ação revelados sob demanda (hover).

---
*Pesquisa efetuada por Pax.*
