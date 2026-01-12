# Mobile App - Sistema de Reconhecimento Facial HDT Energy

## Instalação

1. Instale as dependências: `npm install`
2. Configure o arquivo `.env` com a URL da API
3. Execute o app: `npm start`
4. Escaneie o QR code com o Expo Go ou execute `npm run android` para build nativo

## Build para Android

```bash
npx expo build:android
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```
EXPO_PUBLIC_API_URL=http://seu-ip:8000/api/v1
```

## Permissões

O app requer permissão de câmera para funcionar. A permissão é solicitada automaticamente na primeira execução.

