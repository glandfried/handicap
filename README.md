# handicap

## Agenda

0. Datos de [OGS](https://online-go.com/).
    - Documentar los datos crudos de OGS utilizando siguiendo el _data descriptor template_.
    - Descargar los datos de OGS del 2013 en adelante.

0. Datos de [KGS](https://www.gokgs.com/).
    - Descargar los datos de KGS del año 2000 en adelante. Como referencia debe haber como mínimo 2.3 millones de partidas entre 21/05/2005 y 01/10/2007 (ver paper "Whole-History Ratings").

0. Datos de la [AAgo](http://www.go.org.ar/)
    - Incorporar la base de datos SQL que ofreció la AAgo.

0. Software estado del arte
    - Whole-History Rating [WHR](https://pypi.org/project/whole-history-rating/). 
    - American Go Asociation [AGA](https://www.usgo.org/ratings), versión argentina [AGA-AAgo](https://github.com/elsantodel90/RAAGo/tree/master/original-AGA-rating-system/aago-rating-calculator).
    - Revisar si EGF tiene una solución con handicap. Posible [acá](https://github.com/oris/GoRatings)
    - Revisar si NIHON KI-IN (Japon) tiene solución con handicap
    - Revisar si [KBA](http://english.baduk.or.kr/sub03_04-1.htm) (Corea) tiene soluión con handicap.
    - Solución [OGS](https://forums.online-go.com/t/ogs-has-a-new-glicko-2-based-rating-system/13058) basada en glicko2. 
        - ¿Es posible correr el código?
        - Si no, ¿Es posible saber al menos si considera o no el handicap (en el mejor de los casos está harcodeado)?.  
            - [Acá](https://github.com/online-go/online-go.com/blob/8d5ffa47ccd2d59ef41454d6141183a9e6408ef9/src/lib/rank_utils.ts) definen "get_handicap_adjustment()", que... [Acá](https://github.com/online-go/online-go.com/blob/2ab4a2e291dd183cfc1d40d7d30d99beb31ca72a/src/components/RatingsChart/RatingEntry.ts) se usa en el constructor del RatingEntry que... [Acá](https://github.com/online-go/online-go.com/blob/978cc50179cc5b93e49a207693c72d2ccc5f148c/src/components/RatingsChart/RatingsChart.tsx) se usa en para generar el piechart de contra cuántos mejores o peores ganó/perdió el jugador.

0. Nuestras propuestas.
    - TrueSkill-handicap (ts-h) 
    - TTT-handicap
    - Adaptar [glicko2](https://github.com/sublee/glicko2), glicko2 tal como usamos ts-h, con handicap como miembros del equipo.

0. Análisis (a través de la evidencia).
    - Volver a correr ts-h y compararlo con ts.
    - Correr ttt-h y compararlo con ts-h
    - Correr glicko2-h y compararlo con glicko2 
    - Correr WHR
    - Correr ADA

0. Matener un repositorio funcional

0. Escribir.

0. Publicar.


### Datos

The primary content-type, the *Data Descriptor*, combines traditional narrative content with curated, structured descriptions (metadata) of data to provide a new framework for data sharing and reuse [Submission guidelines](https://www.nature.com/sdata/publish/submission-guidelines).
These principles are designed to align with and support the [FAIR Principles](https://www.nature.com/articles/sdata201618) for scientific data management and stewardship, which declare that research data should be **Findable**, **Accessible**, **Interoperable** and **Reusable** (see [FORCE11](https://www.force11.org/fairprinciples) for details).


### OGS


```bash
grep -r get_handicap_adjustment ./*
./components/RatingsChart/RatingEntry.ts:import {get_handicap_adjustment, effective_outcome, EffectiveOutcome} from 'rank_utils';
./components/RatingsChart/RatingsChart.tsx:    get_handicap_adjustment,
./lib/rank_utils.ts:export function get_handicap_adjustment(rating:number, handicap:number):number {
./lib/rank_utils.ts:    let black_effective_rating: number = black_rating + get_handicap_adjustment(black_rating, handicap);
```

The source code of handicap\_adjustment

```
export function rank_to_rating(rank:number) {
    return 850 * Math.exp(0.032 * rank);
}

export function rating_to_rank(rating:number) {
    return Math.log(Math.min(MAX_RATING, Math.max(MIN_RATING, rating)) / 850.0) / 0.032;
}

export function get_handicap_adjustment(rating:number, handicap:number):number {
    return rank_to_rating(rating_to_rank(rating) + handicap) - rating;
}
```

And effective_outcome

```
grep -r effective_outcome ./* -l
./components/RatingsChart/RatingEntry.ts
./lib/rank_utils.ts
./views/User/User.tsx
```

0. [Handicap](https://forums.online-go.com/t/does-handicap-affect-how-ranked-games-are-rated/13615)
0. [Scoring system](https://forums.online-go.com/t/scoring-system/17323/7)
0. [Ranking and handicap](https://forums.online-go.com/t/ranking-and-handicaps/17739)

