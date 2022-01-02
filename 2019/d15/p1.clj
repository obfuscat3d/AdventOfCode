(defn make-state [mem pc input output rel blocked] 
    {:mem mem :pc pc :input input :output output :rel rel :blocked blocked})
(defn init-state [mem input] (make-state mem 0 input [] 0 false))

(defn load-program [fn] 
  (as-> (slurp fn) $
    (clojure.string/split $ #",")
    (map #(bigint %) $)
    (map vector (range (count $)) $)
    (into (hash-map) $)))

(defn op-code [state] (mod ((:mem state) (:pc state)) 100))
(defn nth-digit [x n] (mod (int (/ x (Math/pow 10 n))) 10))
(defn paw [state n] ; params for writes n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (mem pc) (+ n 1))
      0 (mem (+ n pc) 0)
      1 (mem (+ n pc) 0)
      2 (+ (:rel state) (mem (+ n pc)) 0))))

(defn par [state n] ; params for reads, n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (mem pc) (+ n 1))
      0 (mem (mem (+ n pc)) 0)
      1 (mem (+ n pc) 0)
      2 (mem (+ (:rel state) (mem (+ n pc)) 0)))))

(defn add [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (+ (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn mul [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (* (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn inp [state]
  (if (empty? (:input state))
    (into state { :blocked true })
    (into state {
      :mem (assoc (:mem state) (paw state 1) (first (:input state)))
      :pc (+ 2 (:pc state)) 
      :input (rest (:input state))})))

(defn otp [state]
  ; (prn (par state 1))
  (into state {
    :pc (+ 2 (:pc state)) 
    :output (conj (:output state) (par state 1))}))

(defn jmp-true [state]
  (if (not= 0 (par state 1)) 
    (into state { :pc (par state 2) })
    (into state { :pc (+ (:pc state) 3) })))

(defn jmp-false [state]
  (if (= 0 (par state 1)) 
    (into state { :pc (par state 2) })
    (into state { :pc (+ (:pc state) 3) })))

(defn lt [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (if (< (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn eq [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (if (= (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn rel [state] 
  (into state {
    :pc (+ 2 (:pc state)) 
    :rel (+ (:rel state) (par state 1))}))

(defn halt [state] (into state {:pc -1}))
(defn halted? [state] (= (:pc state) -1))
(def OP-MAP {1 add 2 mul 3 inp 4 otp 5 jmp-true 6 jmp-false 7 lt 8 eq 9 rel 99 halt})
(defn step [state] ((OP-MAP (op-code state)) state))

(defn run [state]
  (loop [state state]
    (if (or (:blocked state) (halted? state)) 
      state
      (recur (step state)))))

;; ----- GENERIC INTCODE ABOVE -----

;; Printing the grid isn't necessary but was handy for debugging movement
(def char-map {0 "#" 1 "." 2 "O" 3 " "})
(defn print-grid [grid]
  (doseq [y (range -25 20)] ; bounds discovered via trial and error
    (doseq [x (range -25 20)]
      (print (if (= [x y] [0 0]) "+" (char-map (grid [x y] 3)) )))
    (println))
  (println))

(defn process-output [u]
  (let [result (first ((u :s) :output))]
    {:s (into (u :s) {:output '()})
     :r (if (= 0 result) 
          (into (u :r) {:moved false}) 
          (into (u :r) {:moved true :p (vec (mapv + ((u :r) :p) ((u :r) :v)))}))
     :g (assoc (u :g) (vec (mapv + ((u :r) :p) ((u :r) :v))) result)}))

; This isn't a general purpose mapping algo, just travels along
; an edge by turning left after every move and progressively going
; clockwise until a valid move is found. Works for this map.
(def dir2vec {1 [0 -1] 2 [0 1] 3 [-1 0] 4 [1 0]})
(def left-next {[0 -1] 3 [0 1] 4 [-1 0] 2 [1 0] 1})
(def right-next {[0 -1] 4 [0 1] 3 [-1 0] 1 [1 0] 2})
(defn make-next-move [u]
  (let [next-map (if ((u :r) :moved) left-next right-next)
        dir (next-map ((u :r) :v))] 
    {:s (into (u :s) {:blocked false :input (list dir)})
     :r (assoc (u :r) :v (dir2vec dir))
     :g (u :g)}))

(defn comp-run [u] (into u {:s (run (u :s))}))

(defn explore [code]
  (loop [u {:s (run (init-state code '(1)))
            :r {:p [0 0] :v [0 1] :moved false}
            :g {[0 0] 1}}]
    (if (and (< 10 (count (u :g))) (= ((u :r) :p) [0 0]))
      (u :g)
      (recur (comp-run (make-next-move (process-output u)))))))

(defn get-neighbors [grid pos]
  (let [[x y] pos
        nbrs #{[(+ x 1) y] [(- x 1) y] [x (+ y 1)] [x (- y 1)]}]
    (filter #(some #{(grid %)} [1 2]) nbrs)))

(defn bfs-all-paths [grid start]
  (loop [queue (conj (clojure.lang.PersistentQueue/EMPTY) [start []])
         seen {}] 
    (let [[cur cur-path] (peek queue)
          path (conj cur-path cur)
          nbrs (get-neighbors grid cur)
          valid-nbrs (map #(list % path) (filter #(not (some #{%} path)) nbrs))
          queue (if (contains? seen cur) (pop queue) (apply conj (pop queue) valid-nbrs))
          seen (if (contains? seen cur) seen (assoc seen cur path))]
      (if (empty? queue)
        seen
        (recur queue seen)))))

(as-> "input" $
 (load-program "input")
 (explore $)
 ; A little hack, we're actually going from the oxygen to [0 0]
 (bfs-all-paths $ (first (filter #(= 2 ($ %)) (keys $))))
 (prn (- (count ($ [0 0])) 1))) ; subtract since the first item in path isn't a move

(as-> "input" $
 (load-program "input")
 (explore $)
 (bfs-all-paths $ (first (filter #(= 2 ($ %)) (keys $))))
 (map count (vals $))
 (prn (- (apply max $) 1)))
