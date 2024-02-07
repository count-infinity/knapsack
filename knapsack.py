from operator import attrgetter

# Run greedy algorithm 
def greedy(items, capacity):  

  metrics = {}
  # Take highest value first  
  sorted_items=sorted(enumerate(items), key=lambda item: item[1].value, reverse=True)
  value, taken = take_until_cap(sorted_items, capacity)


  metrics["greedy_value"] = value

  # Take lowest weight first
  sorted_items=sorted(enumerate(items), key=lambda item: item[1].weight)
  weight_value, weight_taken = take_until_cap(sorted_items, capacity)

  metrics["greedy_weight"] = weight_value

  if weight_value > value:
      value = weight_value
      taken = weight_taken

  # Take lowest weight first
  sorted_items=sorted(enumerate(items), key=lambda item: item[1].value/item[1].weight, reverse=True)
  ratio_value, ratio_taken = take_until_cap(sorted_items, capacity)

  metrics["greedy_ratio"] = ratio_value

  if ratio_value > value:
      value = ratio_value
      taken = ratio_taken


  #print(metrics)
  return (value, taken)



def take_until_cap(items, capacity):
  
  weight = 0
  value = 0
  taken = [0]*len(items)

  for item in items:
        if weight + item[1].weight <= capacity:
            taken[item[0]] = 1
            value += item[1].value
            weight += item[1].weight

  return (value, taken)


  

