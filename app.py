<!DOCTYPE html>
<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Login - SINISTROS AI ENGINE</title>

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:Arial, Helvetica, sans-serif;
        }

        body{
            background:linear-gradient(135deg,#07162d,#020b18);
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
        }

        .login-box{

            width:420px;

            background:#18263d;

            padding:40px;

            border-radius:18px;

            box-shadow:0 0 30px rgba(0,0,0,0.4);

        }

        .logo{

            text-align:center;

            font-size:60px;

            margin-bottom:10px;

        }

        h1{

            color:white;

            text-align:center;

            margin-bottom:10px;

            font-size:38px;

        }

        .subtitulo{

            color:#b9c6d8;

            text-align:center;

            margin-bottom:30px;

            font-size:14px;

        }

        input{

            width:100%;

            padding:15px;

            margin-bottom:18px;

            border:none;

            border-radius:10px;

            font-size:16px;

            outline:none;

        }

        button{

            width:100%;

            padding:15px;

            background:#2da8ff;

            color:white;

            border:none;

            border-radius:10px;

            font-size:18px;

            cursor:pointer;

            transition:0.3s;

        }

        button:hover{

            background:#1593ec;

        }

        .erro{

            background:#ff4d4d;

            color:white;

            padding:12px;

            border-radius:8px;

            margin-bottom:18px;

            text-align:center;

        }

    </style>

</head>

<body>

    <div class="login-box">

        <div class="logo">🔐</div>

        <h1>Login</h1>

        <div class="subtitulo">
            SINISTROS AI ENGINE
        </div>

        {% if erro %}

            <div class="erro">

                {{ erro }}

            </div>

        {% endif %}

        <form method="POST">

            <input
                type="text"
                name="username"
                placeholder="Usuário"
                autocomplete="off"
                required
            >

            <input
                type="password"
                name="senha"
                placeholder="Senha"
                autocomplete="new-password"
                required
            >

            <button type="submit">

                Entrar

            </button>

        </form>

    </div>

</body>

</html>