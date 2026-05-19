-- Script de Inicialização da Base de Dados Supabase para o Omni

-- Tabela para armazenar o histórico de conversas (memória de curto prazo)
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id TEXT NOT NULL, -- Identificador do utilizador (ex: número de WhatsApp)
    role TEXT NOT NULL,      -- 'user', 'assistant', 'tool'
    content TEXT NOT NULL,   -- Conteúdo da mensagem
    timestamp TIMESTAMPTZ DEFAULT now() -- Carimbo de data/hora da mensagem
);

-- Índice para otimizar a busca por sender_id
CREATE INDEX IF NOT EXISTS idx_conversations_sender_id ON conversations (sender_id);

-- Tabela para armazenar as crenças e filosofias extraídas do acervo (memória de longo prazo)
CREATE TABLE IF NOT EXISTS beliefs_acervo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tema TEXT NOT NULL,      -- Tema ou conceito da crença/filosofia
    conteudo TEXT NOT NULL,  -- Descrição detalhada da crença/filosofia
    origem TEXT,             -- Referência de onde foi extraído (ex: 'AcervoCrenças.docx Parte 1')
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Índice para otimizar a busca por tema
CREATE INDEX IF NOT EXISTS idx_beliefs_acervo_tema ON beliefs_acervo (tema);

-- Exemplo de inserção de algumas crenças iniciais (pode ser preenchido manualmente ou via script)
-- INSERT INTO beliefs_acervo (tema, conteudo, origem) VALUES
-- (
--     'Supremacia da Razão',
--     'O maior poder que já experimentei foi subjugar o coração e obedecer apenas à razão. A liberdade não é fazer o que se sente, mas ter a clareza para fazer o que a razão dita.',
--     'AcervoCrenças.docx Parte 1'
-- ),
-- (
--     'Universo de Possibilidades',
--     'Cada objeto de estudo é uma combinação específica de elementos. Adicionar um reagente e a fórmula perde o equilíbrio. Buscar a perspectiva lateral para desestabilizar a visão comum.',
--     'AcervoCrenças.docx Parte 1'
-- ),
-- (
--     'Repetição para Perfeição',
--     'A perfeição não pode ser alcançada sem a prática constante. Cada erro é uma oportunidade de aprendizado e uma chance de descobrir algo novo.',
--     'AcervoCrenças.docx Parte 2'
-- );