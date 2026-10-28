
#   Point   U   Fait    Ce qui manque

1) Register / login + confirmation U3
60% -> 70% -> *75%*
Pas d'étape de confirmation, deux clés de token ('token' et 'badge') + besoin de se log tt le temps

2) Dashboard grid U3
*70%*
Grille 3×3 en dur, sauvegarde en localStorage seulement (pas en base) : changer de navigateur = tout perdre

3) Flow "Add widget" (type → params → refresh rate → confirm) U3
25% -> 30% -> 45% -> 50% -> *55%*
Le drag choisit le type, params et refresh existent une fois posé. Manque le formulaire de config + confirm AVANT l'ajout

4) Reconfigurer un widget U2
0% -> 10% -> 35% -> 45% -> *70%*
Ni validation, ni retour visuel, et config perdue qd déplace

5) Déplacer un widget U2
30% -> 65% -> *70%*
Le drag case → case marche, mais seul le NOM bouge

<!-- 6) Supprimer un widget U2
0% -> *90%*
Fait (bouton × avec aria-label). Pas de confirmation avant suppression -->

7) UI d'abonnement aux services U3
*40%*
Discord OAuth OK. Steam : URL fabriquée côté client, /api/steam/me absent. Aucun catalogue de services

8) Composants widgets par service U3
*50%*
3 vrais widgets, tous avec params configurables donc valides. 3 coquilles Steam vides — sans param elles comptent pour 0

9) Responsive + accessibilité U2
*25%*
3 @media dans index.css, quelques aria-label. Grille figée, drag impossible au clavier. C'est un livrable, pas un bonus

10) Page profil U2
*10%*
profile_panel.jsx = 13 lignes avec "Alexandre" en dur. Le sujet en fait le point d'entrée de l'abonnement

11) Admin U1
0% -> *0%*
Rien. Le sujet dit "would be very useful" → bonus, pas obligatoire

12) Validation client des params U2
0 -> 5% -> *25%*
Register validé (REGEX). Les params widgets non : le champ refresh accepte -5 ou du texte
