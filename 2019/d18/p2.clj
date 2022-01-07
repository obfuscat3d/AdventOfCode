(ns day18 (:require [shams.priority-queue :as pq]))

(defn dims [grid] [(count (grid 0)) (count grid) ])
(defn door? [c] (and (>= (int c) (int \A)) (<= (int c) (int \Z))))
(defn key? [c] (and (>= (int c) (int \a)) (<= (int c) (int \z))))
(defn robot? [c] (= (int c) (int \@)))
(defn wall? [c] (= (int c) (int \#)))
(defn path? [c] (= (int c) (int \.)))
(defn yx-list [grid] (let [[w h] (dims grid)] (for [y (range h) x (range w)] [y x])))
(defn get-nbrs [pos] (let [[y x] pos] #{[(+ y 1) x] [(- y 1) x] [y (+ x 1)] [y (- x 1)]}))

(defn print-grid [grid]
  (let [[width height] (dims grid)]
    (doseq [p (yx-list grid)]
      (when (zero? (last p)) (println))
      (print (get-in grid p)))
    (println)))

(defn slurp-grid [fn]
  (mapv #(vec (char-array %)) (clojure.string/split-lines (slurp fn))))

(defn find-doors [grid]
  (apply conj {}
    (filter #(door? (first (keys %))) 
      (for [p (yx-list grid)] {(get-in grid p) p}))))

(defn find-keys [grid]
  (apply conj 
    (filter #(key? (first (keys %))) 
      (for [p (yx-list grid)] {(get-in grid p) p}))))

(defn find-robots [grid]
  (filter #(robot? (get-in grid %)) (yx-list grid)))

(defn update-grid-robot-key-door [grid start-pos new-pos]
  (let [door-pos ((find-doors grid) (Character/toUpperCase (get-in grid new-pos)))]
    (as-> (if door-pos (assoc-in grid ((find-doors grid) (Character/toUpperCase (get-in grid new-pos))) \.) grid) $
      (assoc-in $ start-pos \.)
      (assoc-in $ new-pos \@))))

(defn update-results [grid start-pos cur]
  (if (key? (get-in grid (cur :pos)))
    [{ :cost (+ (count (cur :path)))
       :grid (update-grid-robot-key-door grid start-pos (cur :pos))
       :removed (get-in grid (cur :pos))
    }]
    [])) ; not a key, no result

(defn filtered-nbrs [grid path pos]
  (do (filter 
    #(and (not (contains? path %))
          (or (key? (get-in grid % \!)) (path? (get-in grid % \!))))
    (get-nbrs pos))))

(defn update-queue [queue grid cur]
  (let [path (conj (cur :path) (cur :pos))
        nbrs (filtered-nbrs grid path (cur :pos)) ]
    (if (key? (get-in grid (cur :pos)))
      (vec (rest queue))
      (reduce conj (vec (rest queue)) (mapv (fn [$] {:pos $ :path path}) nbrs))))) 

;; BFS to find possible moves and associated costs given a grid
(defn available-moves-for-robot [grid start-pos]
  (loop [queue [{:pos start-pos :path #{}}]
        results []]
    (let [cur (first queue)
          new-results (into results (update-results grid start-pos cur))
          new-queue (update-queue queue grid cur)]
      (if (empty? new-queue) 
        new-results
        (recur new-queue new-results)))))

(defn available-moves [grid]
  (reduce into 
    (for [robot (find-robots grid)] 
      (available-moves-for-robot grid robot))))

(defn grid-hash [grid]
  (clojure.string/join (map #(apply str %) grid)))

;; Djikstra's where we treat each grid/move as a node in a graph
(defn shortest-path-for-all-keys [grid]
  ; PQ is always max, so use ($big - cost) so mimic min priority queue
  (loop [pq (pq/priority-queue #(- 1000000 (% :cost)) :elements [{:cost 0 :grid grid}])
         visited #{}]
    (cond 
      (empty? (find-keys ((peek pq) :grid))) ((peek pq) :cost)
      (contains? visited (grid-hash ((peek pq) :grid))) (recur (pop pq) visited)
      :else
        (recur 
          (into 
            (pop pq)
            (mapv (fn [%] {:grid (% :grid) :cost (+ (% :cost) ((peek pq) :cost))})
                  (available-moves ((peek pq) :grid))))
          (conj visited (grid-hash ((peek pq) :grid)))))))

(as-> "input2" $
  (slurp-grid $)
  (shortest-path-for-all-keys $)
  (prn $))
