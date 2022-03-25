from trains.models import Train

def dfs_paths(graph, start, end):
    """
    Поиск всех списков городов через которые можно добраться
    с точки start к точке end
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == end:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    """
    Создание графа
    """
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph

def get_routes(request, form):
    context = {'form': form}
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travel_time = data['total_travel_time']
    all_routes = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_routes):
        raise ValueError('There is no routes satisfies the given parameters')
    if cities:
        """
        Получение списка id городов 
        """
        _cities = [city.id for city in cities]
        ways_through_cities = []
        for route in all_routes:
            if all(city in route for city in _cities):
                ways_through_cities.append(route)
        if not ways_through_cities:
            raise ValueError('There is no routes through the given cities')
    else:
        ways_through_cities = all_routes
    route_trains = []
    all_trains = {}
    """
    Преобразование queryset в словарь, где ключи - сет id городов, 
    значение - поезд с привязанной к нему информацией
    """
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in ways_through_cities:
        tmp = {'trains': []}
        total_time = 0
        for i in range(len(route) - 1):
            train = all_trains[(route[i], route[i + 1])][0]
            total_time += train.travel_time
            tmp['trains'].append(train)
        tmp['total_time'] = total_time
        if total_time <= travel_time:
            route_trains.append(tmp)
    if not route_trains:
        raise ValueError('There is no routes satisfies the given travel time')
    route_trains.sort(key=lambda time: time['total_time'])
    context['routes'] = route_trains
    context['cities'] = {'from_city': from_city, 'to_city': to_city}
    return context

