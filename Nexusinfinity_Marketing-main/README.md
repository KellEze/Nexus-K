# Nexus Infinity Report Viewer

Pequeno aplicativo em Python com interface gráfica Tkinter para exibir informações da empresa Nexus Infinity e um relatório voltado ao setor de Marketing.

## Visão geral

O projeto contém um script principal `show_nexus.py` que apresenta:

- informações da empresa Nexus Infinity
- dados do setor de Marketing
- histórico de análises dos setores
- editor de notas/entrevistas com salvamento em JSON

## Funcionalidades

- janela inicial com opções para mostrar entrevistadores e relatório de marketing
- exibição de dados da empresa e do setor de marketing
- painel de edição para anotações de entrevistas e observações
- salvamento/carregamento local das notas em `marketing_notes.json`
- visualização de histórico de análise e conclusão da equipe

## Requisitos

- Python 3
- biblioteca padrão `tkinter`

> Observação: em sistemas Linux, o pacote `tkinter` pode ser instalado via gerenciador de pacotes se não estiver disponível.

## Execução

No diretório do projeto, execute:

```bash
python3 show_nexus.py
```

## Estrutura do projeto

- `show_nexus.py` — script principal do aplicativo Tkinter
- `marketing_notes.json` — arquivo gerado após salvar as notas (não incluído no repositório inicialmente)

## Uso

1. Abra o aplicativo com `python3 show_nexus.py`.
2. Clique em `Mostrar entrevistadores e apresentação` para ver os dados da empresa e os entrevistadores.
3. Clique em `Relatório do Setor de Marketing` para acessar o relatório, editar notas e visualizar o histórico de análise.
4. Salve as notas para criar/atualizar `marketing_notes.json`.

## Sobre o projeto

O aplicativo foi desenvolvido para registrar e apresentar informações de uma entrevista e análise do setor de Marketing da empresa Nexus Infinity, que trabalha com brinquedos e jogos recicláveis.
