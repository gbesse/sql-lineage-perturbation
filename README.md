# sql-lineage-perturbation

## Français

Mesurer les lignes sources dont dépend réellement un résultat SQLite.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m sql_lineage_perturbation examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Perturbe chaque ligne par suppression dans une vraie base SQLite et compare les sacs de résultats. SQL en lecture seule avec autoriseur, fonctions déterministes autorisées, limite de résultats et budget d’instructions. Un doublon qui masque une dépendance reste explicitement hors preuve de provenance complète.

### Limites

100 lignes sources maximum ; pas d’extension, PRAGMA, accès fichier ou appel réseau. Analyse coûteuse par suppressions isolées, sans prouver toutes les interactions ni expliquer un verdict métier.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Measure source rows on which a SQLite result actually depends.

Synthetic data; no network access or secret required.

```sh
python -m sql_lineage_perturbation examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Deletes each source row in a real SQLite database and compares result bags. Read-only SQL uses an authorizer, allowed deterministic functions, result cap and instruction budget. Redundant support that masks a dependency remains explicitly outside complete provenance.

### Limits

At most 100 source rows; no extensions, PRAGMA, file or network access. Expensive single-deletion analysis, without proving all interactions or explaining business correctness.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Medir las filas fuente de las que depende un resultado SQLite.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m sql_lineage_perturbation examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Elimina cada fila fuente en SQLite real y compara multiconjuntos de resultados. SQL de solo lectura con autorizador, funciones deterministas permitidas y límites de resultados e instrucciones. El soporte redundante queda fuera de una prueba de procedencia completa.

### Límites

Máximo 100 filas fuente; sin extensiones, PRAGMA, archivos ni red. Análisis costoso por eliminación individual, sin probar todas las interacciones ni corrección de negocio.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://www.sqlite.org/c3ref/set_authorizer.html
- https://www.sqlite.org/lang_select.html
