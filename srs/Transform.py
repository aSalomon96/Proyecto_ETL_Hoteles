# Estrategia 1: Resolver conflictos donde un mail tiene más de un id_cliente
# Tomaremos el id_cliente más frecuente para cada correo

# Creamos una función que asigna el id_cliente más frecuente
def resolver_conflictos_mail(group):
    if len(group['id_cliente'].unique()) > 1:
        # Si hay más de un id_cliente, asignamos el id_cliente más frecuente
        id_cliente_frecuente = group['id_cliente'].mode()[0]
        group['id_cliente'] = id_cliente_frecuente
    return group

# Aplicamos la función para resolver los conflictos de mails
df_resuelto_mail = df_hoteles_merg.groupby('mail', group_keys=False).apply(resolver_conflictos_mail)

# Estrategia 2: Resolver conflictos donde un id_cliente tiene más de un mail
# Tomaremos el primer correo asociado a cada id_cliente

# Creamos una función que asigna el primer correo a cada id_cliente
def resolver_conflictos_cliente(group):
    if len(group['mail'].unique()) > 1:
        # Si hay más de un mail, asignamos el primer correo
        primer_mail = group['mail'].iloc[0]
        group['mail'] = primer_mail
    return group


    