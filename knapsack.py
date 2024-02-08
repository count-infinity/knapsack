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
  return (value, taken, 0)



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

def dynamic(items, capacity):
  dtable=[[0 for i in range(len(items))] for j in range(capacity+1)] 

  for idx, item in enumerate(items):
    # Too heavy to ever take
    if item.weight > capacity: continue

    for weight in range(capacity+1):

      if item.weight > weight:
        if idx !=0:
          dtable[weight][idx]=dtable[weight][idx-1]
        continue
                 
      # First item
      if idx == 0:        
        dtable[weight][idx] = item.value
        continue

      

      prev_item_idx = idx-1
      prev_idx_without_weight = max(weight-item.weight,0)

      
      prev_best_value = dtable[weight][prev_item_idx]
      prev_best_value_without_weight = dtable[prev_idx_without_weight][prev_item_idx]

      best_value_if_chosen = prev_best_value_without_weight + item.value

      dtable[weight][idx] = max(prev_best_value, best_value_if_chosen)  

  value, selection = determine_picked(dtable, items)
  return (value, selection, 1)

def determine_picked(dtable, items):  

  current_weight = len(dtable)-1

  item_taken=[]
  max_value = 0 

  for item in reversed(items):

    if item.weight > len(dtable):
       item_taken.append(0)
       continue
    
    item_idx = item.index 
    current_val = dtable[current_weight][item_idx]
    if (current_val > max_value): max_value = current_val
    prev_val = 0

    if item_idx > 0:    
       prev_val = dtable[current_weight][item_idx-1]

    if current_val != prev_val:
      current_weight -= item.weight      
      item_taken.append(1)
    else:
      item_taken.append(0)
  
  return (max_value, reversed(item_taken))


def min_max(items):
  min_weight = float('inf')
  max_weight = 0
  for item in items:
    if item.weight < min_weight:
      min_weight = item.weight
    if item.weight > max_weight:
      max_weight = item.weight
  
  return (min_weight, max_weight, max_weight*len(items))
        





       
      
      








      



    





  

