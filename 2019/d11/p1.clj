(defn make-state [mem pc input output rel blocked] 
    {:mem mem :pc pc :input input :output output :rel rel :blocked blocked})
(defn update-state [state delta] (into state delta))
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
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (+ (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn mul [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (* (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn inp [state]
  (if (empty? (:input state))
    (update-state state { :blocked true })
    (update-state state {
      :mem (assoc (:mem state) (paw state 1) (first (:input state)))
      :pc (+ 2 (:pc state)) 
      :input (rest (:input state))})))

(defn otp [state]
  ; (prn (par state 1))
  (update-state state {
    :pc (+ 2 (:pc state)) 
    :output (conj (:output state) (par state 1))}))

(defn jmp-true [state]
  (if (not= 0 (par state 1)) 
    (update-state state { :pc (par state 2) })
    (update-state state { :pc (+ (:pc state) 3) })))

(defn jmp-false [state]
  (if (= 0 (par state 1)) 
    (update-state state { :pc (par state 2) })
    (update-state state { :pc (+ (:pc state) 3) })))

(defn lt [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (if (< (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn eq [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (if (= (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn rel [state]
  (update-state state {
    :pc (+ 2 (:pc state))
    :rel (+ (:rel state) (par state 1))}))

(defn halt [state] (update-state state {:pc -1}))
(defn halted? [state] (= (:pc state) -1))
(def OP-MAP {1 add 2 mul 3 inp 4 otp 5 jmp-true 6 jmp-false 7 lt 8 eq 9 rel 99 halt})
(defn step [state] ((OP-MAP (op-code state)) state))

(defn run [state]
  (loop [state state]
    (if (or (:blocked state) (halted? state)) 
      state
      (recur (step state)))))

;; ----- EVERYTHIGN ABOVE HERE IS GENERIC INTCODE -----

(defn update-tiles [$]
  (let [r ($ :robot)]
    (assoc ($ :tiles) [(r :x) (r :y)] (first (($ :comp) :output)))))

(defn update-robot [$] ; 0 left, 1 right
  (let [r ($ :robot)
        right? (= 1 (last (($ :comp) :output)))
        new-dx (if right? (r :dy) (- 0 (r :dy)))
        new-dy (if right? (- 0 (r :dx)) (r :dx))]
    {:dx new-dx :dy new-dy :x (+ (r :x) new-dx) :y (+ (r :y) new-dy)}))

(defn update-comp [$]
  (let [r ($ :robot)
        t ($ :tiles)]
    (update-state ($ :comp) {:blocked false 
                             :output []
                             :input (list (t [(r :x) (r :y)] 0)) })))

(defn run-bot [input]
  (loop [state {:comp (init-state (load-program "input") input)
                :robot {:dx 0 :dy 1 :x 0 :y 0}
                :tiles {}}]
    (if (halted? (state :comp))
      (state :tiles)
      (recur (as-> state $
               (assoc $ :comp (run ($ :comp)))
               (assoc $ :tiles (update-tiles $))
               (assoc $ :robot (update-robot $))
               (assoc $ :comp (update-comp $))               
               )))))

(defn print-tiles [tiles] 
  (doseq [x (range 5 -10 -1)]
    (doseq [y (range -10 80)]
      (print (if (= 1 (tiles [y x])) "#" " ")))
    (prn)))

(println "Part 1: " (count (run-bot '(0))))
(println "Part 2: ")
(print-tiles (run-bot '(1)))