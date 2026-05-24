# omskills

Skills pessoais do the maintainer para trabalhar com Codex e outros agentes sem sair dos trilhos.

## Origem

Este repositorio e basicamente um fork/adaptacao de [mattpocock/skills](https://github.com/mattpocock/skills), copiado como estava em 24 de maio de 2026, e esta sendo adaptado aos casos de uso do the maintainer.

the maintainer nao criou a base original destas skills. Este nao e o repo original; para ver o projeto de origem, use [mattpocock/skills](https://github.com/mattpocock/skills).

Os repos devem divergir bastante ao longo do tempo. O repo original deve continuar separado para acompanhar upstream; este aqui e o espaco pessoal do the maintainer para ajustar nomes, rituais, triage e instalacao ao proprio workflow.

## Workflow the maintainer

O fluxo que este repo deve reforcar:

`ideia -> grill -> docs -> issue -> branch -> PR -> handoff`

Regra mental:

- Quero pensar: `/grill-with-docs`
- Quero organizar fila: `/triage`
- Quero decidir arquitetura: `/improve-codebase-architecture`
- Quero implementar issue madura: `/tdd`
- Algo quebrou: `/diagnose`
- Vou parar: `/handoff`

Regra de seguranca para repos como `omnews`: se a tarefa tocar arquitetura, comportamento compartilhado, Docker/runtime, AI runners, TTS, persistencia ou fluxo de publish, nao implemente direto. Primeiro verifique issue existente, trie a issue, use `/grill-with-docs` se houver ambiguidade, registre linguagem/decisoes em `CONTEXT.md` ou `docs/adr/`, e so entao siga para branch + PR.

Se aparecer conflito, ambiguidade arquitetural, dependencia nao resolvida ou duas opcoes plausiveis com tradeoffs reais, pare e converse.

## Quickstart Local

1. Linke as skills ativas para o Codex local:

```bash
./scripts/link-skills.sh
```

Por padrao o script escreve em `~/.codex/skills`. Para testar em outro destino:

```bash
OMSKILLS_DEST=/tmp/omskills-test ./scripts/link-skills.sh
```

2. Em cada repo que vai consumir estas skills, rode:

```text
/setup-omskills
```

Esse setup registra onde ficam issues, quais labels de triage o repo usa, e como o agente deve consumir `CONTEXT.md` e ADRs.

## Modelo De Triage

As skills usam cinco papeis canonicos. Cada repo pode mapear esses papeis para labels reais em `docs/agents/triage-labels.md`.

- `needs-triage`: mantenedor precisa avaliar.
- `needs-info`: falta informacao do reporter/autor.
- `ready-for-agent`: issue bem especificada, pronta para um agente implementar sem contexto extra.
- `ready-for-human`: precisa de implementacao ou decisao humana.
- `wontfix`: nao sera feita.

Para `omnews`, a fila deve favorecer issues pequenas, verticais e verificaveis. Issues de runtime, AI runners, TTS, persistencia, Docker e publish precisam estar maduras antes de implementacao.

## Skills Ativas

### Engineering

- **[diagnose](./skills/engineering/diagnose/SKILL.md)**: loop disciplinado para bugs e regressoes: reproduzir, minimizar, hipotetizar, instrumentar, corrigir e criar teste de regressao.
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: entrevista o usuario, cruza respostas com o codigo quando possivel, afia linguagem de dominio e atualiza `CONTEXT.md`/ADRs quando decisoes cristalizam.
- **[triage](./skills/engineering/triage/SKILL.md)**: processa issues por uma maquina de estados baseada nos papeis de triage.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: encontra oportunidades de aprofundar modulos e reduzir acoplamento, usando `CONTEXT.md` e ADRs como contexto.
- **[setup-omskills](./skills/engineering/setup-omskills/SKILL.md)**: configura issue tracker, labels de triage e layout de docs por repo.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: desenvolvimento com red-green-refactor, em fatias verticais pequenas.
- **[to-issues](./skills/engineering/to-issues/SKILL.md)**: quebra planos, specs ou PRDs em issues independentes.
- **[to-prd](./skills/engineering/to-prd/SKILL.md)**: transforma o contexto da conversa em PRD e publica no issue tracker.
- **[zoom-out](./skills/engineering/zoom-out/SKILL.md)**: pede uma perspectiva de sistema antes de mexer em uma area desconhecida.
- **[prototype](./skills/engineering/prototype/SKILL.md)**: cria prototipos descartaveis para validar logica, estado ou alternativas de UI.

### Productivity

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: entrevista rigorosa para amadurecer uma ideia sem necessariamente tocar codigo.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: compacta a sessao em um handoff para outro agente continuar.
- **[write-a-skill](./skills/productivity/write-a-skill/SKILL.md)**: cria novas skills com estrutura, frontmatter e recursos auxiliares.

## Skills Opcionais

Mantidas como inspiracao ou para uso pontual, mas fora do manifest Codex principal por enquanto:

- **[caveman](./skills/productivity/caveman/SKILL.md)**
- **[setup-pre-commit](./skills/misc/setup-pre-commit/SKILL.md)**
- **[git-guardrails-claude-code](./skills/misc/git-guardrails-claude-code/SKILL.md)**
- **[scaffold-exercises](./skills/misc/scaffold-exercises/SKILL.md)**
- **[migrate-to-shoehorn](./skills/misc/migrate-to-shoehorn/SKILL.md)**

Ignorar por enquanto:

- `skills/deprecated/`
- `skills/personal/`
- `skills/in-progress/`

## Manutencao

Quando uma skill ativa for renomeada ou promovida, atualize em conjunto:

- pasta da skill
- frontmatter `name`
- README principal
- README do bucket
- `.codex-plugin/plugin.json`
- referencias duras em outras skills, ADRs, scripts e docs
