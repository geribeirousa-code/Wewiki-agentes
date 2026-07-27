import os
import re
from datetime import datetime, timezone

def parse_frontmatter(content):
    frontmatter = {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    fm_text = match.group(1)
    for line in fm_text.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            # Basic parsing of strings, lists, etc.
            if val.startswith("[") and val.endswith("]"):
                val = [item.strip().strip('"').strip("'") for item in val[1:-1].split(",") if item.strip()]
            elif val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val.lower() == "null":
                val = None
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            else:
                try:
                    val = int(val)
                except ValueError:
                    pass
            frontmatter[key] = val
    return frontmatter

def main():
    workspace = r"c:\Users\gerib\OneDrive\Desktop\GE NEGOCIOS\AGENTES"
    tasks_dir = os.path.join(workspace, "Wiki equipe", "tarefas")
    
    categories = ["abertas", "em-andamento", "concluidas", "canceladas"]
    tasks_data = []
    
    for cat in categories:
        cat_dir = os.path.join(tasks_dir, cat)
        if not os.path.exists(cat_dir):
            continue
        
        # We need to search recursively for completed and canceled tasks (nested under YYYY/MM)
        for root, dirs, files in os.walk(cat_dir):
            for file in files:
                if file.startswith("tsk-") and file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    fm = parse_frontmatter(content)
                    if fm:
                        fm["filepath"] = filepath
                        fm["rel_path"] = os.path.relpath(filepath, tasks_dir).replace("\\", "/")
                        fm["filename_slug"] = os.path.splitext(file)[0]
                        # Correct status if needed based on directory
                        expected_status = {
                            "abertas": "aberta",
                            "em-andamento": "em-andamento",
                            "concluidas": "concluida",
                            "canceladas": "cancelada"
                        }[cat]
                        
                        if fm.get("status") != expected_status:
                            # Update frontmatter in file
                            # For simplicity we just note it or we can actually edit the file as per SOP
                            old_status = fm.get("status")
                            fm["status"] = expected_status
                            # Replace in file content
                            updated_content = re.sub(
                                r"^status:\s*.*$",
                                f"status: {expected_status}",
                                content,
                                flags=re.MULTILINE
                            )
                            # Update timestamp
                            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                            updated_content = re.sub(
                                r"^atualizado:\s*.*$",
                                f"atualizado: {now_str}",
                                updated_content,
                                flags=re.MULTILINE
                            )
                            # Append history log
                            log_line = f"\n- {datetime.now().strftime('%Y-%m-%d %H:%M')} (reconstrução) — campo status corrigido para corresponder à pasta (de {old_status} para {expected_status})"
                            updated_content += log_line
                            
                            with open(filepath, "w", encoding="utf-8") as f_out:
                                f_out.write(updated_content)
                            print(f"Corrigido status de {file} para {expected_status}")
                        
                        tasks_data.append((cat, fm))
    
    # Sort and filter
    abertas = [t for cat, t in tasks_data if cat == "abertas"]
    # Sort abertas by priority (ascending, 1 is highest) then created date
    abertas.sort(key=lambda x: (x.get("prioridade", 4), x.get("criado", "")))
    
    em_andamento = [t for cat, t in tasks_data if cat == "em-andamento"]
    # Sort em-andamento by updated date descending
    em_andamento.sort(key=lambda x: x.get("atualizado", ""), reverse=True)
    
    concluidas = [t for cat, t in tasks_data if cat == "concluidas"]
    canceladas = [t for cat, t in tasks_data if cat == "canceladas"]
    
    # Recently closed (last 7 days)
    recently_closed = []
    now = datetime.now(timezone.utc)
    
    def parse_dt(dt_str):
        if not dt_str:
            return datetime.min.replace(tzinfo=timezone.utc)
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

    for cat, t in tasks_data:
        if cat in ["concluidas", "canceladas"]:
            closed_time = parse_dt(t.get("atualizado"))
            delta = now - closed_time
            if delta.days <= 7:
                recently_closed.append((closed_time, t))
                
    recently_closed.sort(key=lambda x: x[0], reverse=True)
    
    # Render INDEX.md
    out = []
    out.append("# Índice de Tarefas\n")
    out.append("_Gerado automaticamente. Não edite manualmente. Execute `SOP-reconstruir-indice-tarefas` para regenerar._\n")
    out.append(f"_Última reconstrução: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}_\n")
    
    # Summary
    # Count of this month's completed/canceled
    this_month_concluidas = 0
    this_month_canceladas = 0
    for cat, t in tasks_data:
        dt = parse_dt(t.get("atualizado"))
        if dt.year == now.year and dt.month == now.month:
            if cat == "concluidas":
                this_month_concluidas += 1
            elif cat == "canceladas":
                this_month_canceladas += 1
                
    bloqueadas_count = sum(1 for t in em_andamento if t.get("motivo_bloqueio"))
    
    out.append("## Resumo")
    out.append(f"- Abertas: {len(abertas)}")
    out.append(f"- Em andamento: {len(em_andamento)} ({bloqueadas_count} bloqueadas)")
    out.append(f"- Concluídas (este mês): {this_month_concluidas}")
    out.append(f"- Canceladas (este mês): {this_month_canceladas}\n")
    
    # Abertas
    out.append(f"## Abertas ({len(abertas)})")
    if not abertas:
        out.append("_(nenhuma ainda — veja [[SOP-criar-tarefa]] para adicionar uma)_")
    else:
        priorities = {1: "urgente", 2: "alta", 3: "normal", 4: "baixa"}
        for prio in [1, 2, 3, 4]:
            prio_tasks = [t for t in abertas if t.get("prioridade") == prio]
            if prio_tasks:
                out.append(f"\n### Prioridade {prio} — {priorities[prio]}")
                for t in prio_tasks:
                    slug = t["filename_slug"]
                    assignee = t.get("atribuido_a") or "não atribuído"
                    criado = t.get("criado", "")[:10]
                    out.append(f"- [[Wiki equipe/tarefas/abertas/{slug}|{slug}]] — {t.get('titulo')} — responsável: {assignee} — criada {criado}")
    out.append("")
    
    # Em andamento
    out.append(f"## Em andamento ({len(em_andamento)})")
    if not em_andamento:
        out.append("_(nenhuma)_")
    else:
        for t in em_andamento:
            slug = t["filename_slug"]
            assignee = t.get("atribuido_a") or "não atribuído"
            if t.get("motivo_bloqueio"):
                out.append(f"- [[Wiki equipe/tarefas/em-andamento/{slug}|{slug}]] — responsável: {assignee} — BLOQUEADA: {t.get('motivo_bloqueio')}")
            else:
                atualizado = t.get("atualizado", "")[:10]
                out.append(f"- [[Wiki equipe/tarefas/em-andamento/{slug}|{slug}]] — responsável: {assignee} — assumida {atualizado}")
    out.append("")
    
    # Por responsável
    out.append("## Por responsável")
    assignees = {}
    for cat, t in tasks_data:
        if cat in ["abertas", "em-andamento"]:
            assignee = t.get("atribuido_a") or "não atribuído"
            if assignee not in assignees:
                assignees[assignee] = {"abertas": 0, "em-andamento": 0, "bloqueadas": 0}
            assignees[assignee][cat] += 1
            if cat == "em-andamento" and t.get("motivo_bloqueio"):
                assignees[assignee]["bloqueadas"] += 1
                
    if not assignees:
        out.append("_(nenhum responsável ativo)_")
    else:
        for name, counts in sorted(assignees.items()):
            out.append(f"- {name}: {counts['abertas']} abertas, {counts['em-andamento']} em andamento ({counts['bloqueadas']} bloqueadas)")
    out.append("")
    
    # Recentemente fechadas
    out.append("## Recentemente fechadas (últimos 7 dias)")
    if not recently_closed:
        out.append("_(nenhuma)_")
    else:
        for dt, t in recently_closed:
            slug = t["filename_slug"]
            status = t["status"]
            by = t.get("atualizado_por") or t.get("atribuido_a") or "sistema"
            dt_str = dt.strftime("%Y-%m-%d")
            out.append(f"- {dt_str} [[Wiki equipe/tarefas/{status}s/{slug}|{slug}]] — {status} — {by}")
    
    index_path = os.path.join(tasks_dir, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(out))
    print("Índice de tarefas reconstruído com sucesso!")

if __name__ == "__main__":
    main()
