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

;; ----- GENERIC INTCODE ABOVE -----

(defn update-board [board new-output]
  (reduce #(into %1 {[(nth %2 0) (nth %2 1)] (nth %2 2)}) board (partition 3 new-output)))

(def char-map {0 " " 1 "#" 2 "@" 3 "-" 4 "O"})
(defn print-board [board]
  (println)
  (doseq [y (range 20)]
    (doseq [x (range 50)]
      (print (char-map (board [x y] 0))))
    (println))
  (println)
  (println "Score: " (board [-1 0])))

(defn process-input [board state]
  (let [ball-x (first (first (filter #(= 4 (board %)) (keys board))))
        paddle-x (first (first (filter #(= 3 (board %)) (keys board))))
        dx (if (= ball-x paddle-x) 0 (if (< paddle-x ball-x) 1 -1))]
    (update-state state {:output [] :input [dx] :blocked false})))

(defn play-game [state]
  (loop [state (run state)
         board {}]
    (let [board (update-board board (state :output))]
      (print-board board)
      (recur(run (process-input board state)) board))))

(play-game (init-state (load-program "input") []))
