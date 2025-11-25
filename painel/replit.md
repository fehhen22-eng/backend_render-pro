# H2H Insights Hub - Painel de Análise H2H

## Visão Geral
Painel de insights e predição para análise de confrontos head-to-head (H2H) com estatísticas avançadas e inteligência artificial.

## Tecnologias
- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **UI Framework**: shadcn-ui (componentes Radix UI)
- **Styling**: Tailwind CSS
- **Roteamento**: React Router v6
- **Gráficos**: Recharts
- **Formulários**: React Hook Form + Zod
- **Estado**: TanStack Query

## Estrutura do Projeto
```
/
├── src/
│   ├── components/     # Componentes React
│   │   ├── ui/        # Componentes shadcn-ui
│   │   └── ...        # Componentes customizados
│   ├── hooks/         # React hooks customizados
│   ├── lib/           # Utilitários e helpers
│   ├── pages/         # Páginas da aplicação
│   ├── App.tsx        # Componente principal
│   └── main.tsx       # Entry point
├── public/            # Assets estáticos
└── vite.config.ts     # Configuração Vite
```

## Funcionalidades
- **Palpites do Dia**: Sugestões de apostas baseadas em análise
- **Apostas Múltiplas**: Sistema de combinação de apostas
- **Análise de Confronto**: Análise detalhada H2H entre times
- **Importação de Dados**: Importação de ligas/CSV

## Configuração Replit
O projeto está configurado para rodar no Replit com:
- Porta: 5000 (obrigatório para webview)
- Host: 0.0.0.0 (permite acesso externo)
- allowedHosts: true (permite proxy do Replit)
- HMR com configurações padrão do Vite (otimizado para Replit)

**Nota**: É normal ver mensagens temporárias de "[vite] server connection lost" durante reinicializações do workflow ou quando o preview perde foco. O Vite reconecta automaticamente em milissegundos e o HMR funciona normalmente.

## Comandos Disponíveis
- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Build para produção
- `npm run preview` - Preview do build de produção
- `npm run lint` - Executa linter ESLint

## Data de Instalação
22 de novembro de 2025

## Alterações Recentes
- **22/11/2025**: Instalação inicial e configuração para Replit
  - Extraído arquivos do ZIP
  - Configurado Vite para porta 5000 com HMR
  - Instalado Node.js 20 e todas as dependências
  - Workflow configurado e testado
