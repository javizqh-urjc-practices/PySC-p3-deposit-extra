[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/-Bce75SB)
# P3 - Depósito 2.0

En esta práctica vamos a partir de la solución de la práctica anterior basada en acciones durativas. Crea un fichero llamado [deposit_domain.pddl](deposit_domain.pddl) para la definición del dominio y otro llamado [deposit_problem.pddl](deposit_problem.pddl) para la definición del problema, e incluye tu solución de la última práctica.

## Ejercicio 1
Si aún no has hecho el ejercicio extra de la P2, modifica la duración de la acción `move` para que dependa de la distancia entre el origen y el destino. Además, añade un predicado para saber si dos ubicaciones están conectadas. La acción `move` sólo se podrá realizar si el origen y el destino están conectados.

## Ejercicio 2
Modifica el [problema](deposit_problem.pddl) para que el `goal` no esté expresado para cada objeto de forma individual, sino para todos a la vez (usando forall).
Prueba a generar el plan con POPF y con OPTIC y comenta las diferencias.

*[Respuesta]*

Con POPF el planificador da segmentation fault al no estar el forall correctamente soportado:
```bash
Constructing lookup tables: [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%] [110%] [120%] [130%] [140%]
[ros2run]: Segmentation fault
```

Mientras que con OPTIC el plan se genera de forma correcta:
```bash
0.000: (move walle table floor)  [10.000]
10.001: (pick rotten_apple floor walle)  [2.000]
12.002: (load rotten_apple walle)  [1.000]
13.003: (pick newspaper floor walle)  [2.000]
15.004: (load newspaper walle)  [1.000]
16.005: (pick bottle floor walle)  [2.000]
18.006: (load bottle walle)  [1.000]
19.007: (move walle floor large-deposit)  [50.000]
69.008: (unload rotten_apple walle)  [1.000]
69.008: (unload newspaper walle)  [1.000]
69.008: (unload bottle walle)  [1.000]
```


## Ejercicio 3
No nos terminamos de fiar de los planificadores, ya que a veces nos dan planes en los que el robot no termina de llenar su contenedor antes de volver al depósito.
Por este motivo, vamos a modificar el dominio para que sea más restrictivo, y no vamos a permitir al robot volver a su base hasta que no haya recogido todos los objetos.

Implementa una acción adicional para que el robot vuelva a su base, donde está el depósito. Esta acción sólo se podrá realizar una vez que todos los objetos de tipo `item` hayan sido recogidos por el robot.
Explica cómo has definido los requisitos para que se cumpla la restricción propuesta:


*[Respuesta]*

Para que se cumpla la restricción lo primero que hay que hacer es que la acción move no funcione para la localización del deposito. Esto se consigue añadiendo a la condición la siguiente línea:
```pddl
(at start (not (= ?to Large-deposit)))
```

Luego se crea la nueva acción a la que se pone la condición contraria y se le añade la condición de tener todos los objetos cargados en el robot:
```pddl
(at start (forall (?it - item) (robot_store ?r ?it)))
(at start (= ?to Large-deposit))
```

*Nota:* Esta acción tiene el objetivo de evitar que el robot vaya al depósito a descargar (`unload`) hasta que no haya recogido toda la basura. Si se te ocurre una solución alternativa, impleméntala y explica su funcionamiento.

*Pistas:*
* Es posible definir el depósito principal como una constante.
* Si añadimos la restricción de que todos los objetos deben ser cargados en el robot antes de ir al depósito, es posible que haya que aumentar la capacidad máxima de carga del robot para que el problema tenga solución.



## Ejercicio extra [*Opcional*]
Implementa en [UPF](https://unified-planning.readthedocs.io/en/latest/) alguno de los dominios/problemas usados en las últimas 3 prácticas y compara los resultados.
