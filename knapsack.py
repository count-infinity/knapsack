from collections import namedtuple
Node = namedtuple("Node", ['value', 'capacity', 'estimate', 'index', 'take','path'])

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

  # Take lowest ratio first
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
  print(len(dtable[0]))
  print(len(dtable))

  for idx, item in enumerate(items):    

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

      #print(dtable)
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


def reorder(sorted_items, path):

  new_path=[0]*len(sorted_items)
  for idx, take in enumerate(path):    
      new_path[sorted_items[idx].index]=take
  
  return new_path


# Branch and bound
def bnb(items, capacity):
  # Take highest ratio first
  sorted_items=sorted(items, key=lambda item: item.value/item.weight, reverse=True)

  root = Node(0,capacity,best_estimate(sorted_items, capacity), -1,-1,[])
  print(f"Root best estimate: {root.estimate}")


  queue = [root]

  best_node = None
  best_value = 0

  bvs = 0


  while len(queue) > 0:
    current_node = queue.pop()    
    child_index = current_node.index+1

    if current_node.value > best_value:
      best_value = current_node.value
      best_node = current_node
    
    if child_index == len(sorted_items):            
      continue 
       
    item = sorted_items[child_index]
    
    selected = Node(current_node.value+item.value, current_node.capacity-item.weight, current_node.estimate,child_index,1,current_node.path+[1])           
    not_selected = Node(current_node.value, current_node.capacity, current_node.value+best_estimate(sorted_items[child_index+1:], current_node.capacity),child_index,0,current_node.path+[0])

    

    if not_selected.estimate >= best_value:
      queue.append(not_selected)    
    
    if selected.capacity >= 0: #and selected.estimate >= best_value:
      if selected.value > bvs: bvs=selected.value
      queue.append(selected)


  best_path=reorder(sorted_items,best_node.path)
  print(f"BVS {bvs}")
  return (best_node.value,best_path,1)
    
      

def best_estimate(items, capacity_left):

  print(f"\nCapacity left: {capacity_left}")
  print([str(i.weight)+":"+str(i.value) for i in items])

  estimate = 0
  for item in items:    
    capacity_left -= item.weight
    if capacity_left >= 0:
      estimate += item.value
    else:      
      difference = abs(capacity_left)
      fraction = difference/item.weight
      estimate += fraction*item.value
      print(f"Difference {difference}, fraction {fraction}, est {estimate}")
      break
  #print(f"Estimate: {estimate}")
  return estimate


   

   

   




       
      
      








      



    





  

