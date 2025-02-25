-- BONUS TRACK 1

--01. Cuantos hoteles tiene la base de datos
select 
	count(id_hotel)
from hoteles h 
-- RESULTADO: 29 hoteles*


--02. Cuantas reservas se han hecho
select 
	count(id_reserva) 
from reservas r 
-- RESULTADO: 14.925 reservas


--03. Identifica los 10 clientes que más se han gastado
select 
    concat(c.nombre, ' ', c.apellido) AS nombre_completo,
    c.id_cliente AS id_cliente,
    sum(r.precio_noche) AS total_precio_noche
from 
    clientes c
inner join reservas r ON c.id_cliente = r.id_cliente
group by 
    c.nombre, c.apellido, c.id_cliente
order by 3 desc
limit 10;


-- 04.Identifica el hotel de la competencia y el hotel de nuestra marca que más han recaudado para esas fechas
with RevenueByHotel AS (
    select
    	h.id_hotel,
        h.nombre_hotel AS hotel_name,
        h.competencia,
        SUM(r.precio_noche) AS total_revenue
    from
        hoteles h
    inner join
        reservas r on h.id_hotel = r.id_hotel
    group by 
        h.id_hotel, h.nombre_hotel, h.competencia
),
MaxRevenueByType as (
    select
        competencia,
        MAX(total_revenue) AS max_revenue
    from
        RevenueByHotel
    group by
        competencia
)
select
    rbh.id_hotel,
    rbh.hotel_name,
    rbh.competencia,
    rbh.total_revenue
from
    RevenueByHotel rbh
inner join
    MaxRevenueByType mrbt ON rbh.competencia = mrbt.competencia AND rbh.total_revenue = mrbt.max_revenue;
-- RESULTADO
--12	Hotel Monte Verde					false	151030.36
--131	ibis budget Madrid Centro Lavapies	true	89956.0



--05. Identifica cuantos eventos hay.
select count(id_evento) 
from eventos e 
-- RESULTADO: 221 eventos


--06. Identifica el día que más reservas se han hecho para nuestro hoteles
select 
	fecha_reserva, 
	count(r.id_reserva)
from reservas r 
inner join hoteles h on h.id_hotel = r.id_hotel 
where h.competencia = false 
group by 1
order by 2 desc
limit 1
-- RESULTADO: 2025-02-06
