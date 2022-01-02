(ns day-14 (:require [clojure.string :as str]))

(defn parse-inputs [inputs]
  (as-> (map #(str/split % #" ") inputs) $
    (map #(list (Integer/parseInt (first %)) (last %))  $)))

(defn add-rule [rules line]
  (let [sides (str/split line #" => " )
        output (str/split (last sides) #" " )
        inputs (str/split (first sides) #", ") ] 
    (into rules {
      (last output)
      { :qty (Integer/parseInt (first output))
        :inputs (parse-inputs inputs)}})))

(defn make-rules [input]
  (loop [rules {}
         lines (str/split-lines input)]
    (if (empty? lines)
      rules
      (recur (add-rule rules (first lines)) (rest lines)))))

(defn add-to-map [m k v] (assoc m k (+ (m k 0) v)))

(defn add-new-needs [needs units inputs]
  (loop [needs needs
         inputs inputs]
    (if (empty? inputs) 
      needs
      (recur (add-to-map needs (last (first inputs)) (* units (first (first inputs))))
             (rest inputs)))))

(defn use-extra [need need-qty rules extra needs]
  (if (contains? extra need)
    (if (<= need-qty (extra need 0))
      [need 0 rules (assoc extra need (- (extra need) need-qty)) needs]
      [need (- need-qty (extra need)) rules (assoc extra need 0) needs])
    [need need-qty rules extra needs]))

(defn next-multiple [a b] (if (= 0 (mod a b)) a (+ a (- b (mod a b)))))
(defn make-need [need need-qty rules extra needs]
  (let [unit-qty ((rules need) :qty)
        make-qty (next-multiple need-qty unit-qty)
        extra-qty (- make-qty need-qty)
        units (/ make-qty unit-qty)
        inputs ((rules need) :inputs)]
    [(add-to-map extra need extra-qty) 
     (dissoc (add-new-needs needs units inputs) need)]))

(defn ore-for-fuel [rules]
  (loop [needs {"FUEL" 1}
         extra {}]
    (if (empty? (filter #(and (> (needs %) 0) (not= % "ORE")) (keys needs)))
      needs
      (let [need (first (filter #(and (< 0 (needs %)) (not= % "ORE")) (keys needs)))
            need-qty (needs need)]
        (as-> (use-extra need need-qty rules extra needs) $
          (apply make-need $)
          (recur (nth $ 1) (nth $ 0)))))))

(as-> (slurp "input") $
  (make-rules $)
  (ore-for-fuel $)
  (prn $))
