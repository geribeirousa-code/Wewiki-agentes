# Schema de Dados — App Financeiro Pessoal (Em Progresso)

**Disparado:** 2026-07-27  
**Responsável:** Silas  
**Status:** 🔄 Estruturando

## Brief

Estruturar o schema de dados MÍNIMO para o MVP. Sem over-engineer, apenas o necessário para:
- Criar conta + autenticação
- Registrar transações
- Calcular análises básicas
- Suportar multi-idioma + multi-moeda
- Armazenar preferências de usuário

## Requisitos

1. **Mínimo viável** — Não adicione campos que não serão usados no MVP
2. **Normalizad** — Evite duplicação (usar IDs, não strings)
3. **Performance** — Índices para queries frequentes (gastos por mês, por categoria, por usuário)
4. **Extensível** — Estrutura que suporte adicionar campos depois (tags, anexos, goals)

## Deliverables (em construção)

_Aguardando schema de Silas..._

---

**Próxima ação:** Definir stack técnico (PostgreSQL? SQLite? Firebase?) + migrations.
