using Datalayer;
using Datalayer.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Middleware
{
    public class ProjectService : IProjectService
    {
        private AggDbContext _dbContext;
        public ProjectService(AggDbContext dbContext)
        {
            _dbContext = dbContext;
        }
        public async Task<IEnumerable<Project>> GetProjects(
            IEnumerable<Predicate<string>> filters,
            int skipElements,
            int elementsToTake)
        {
            //TODO: Investigate dynamic lambda expressions
            //TODO: How to generalize the filtering?
            //TODO: skip/take for pagination
            var filteringFunction = delegate (string v)
            {
                return filters.Any(f => f(v));
            };

            var categories = await _dbContext.Categories.Where(
                t => t.GetFilterable().Any(
                    x => filteringFunction(x)
                    )
                ).Select(c => c.Id).ToListAsync();

            return await _dbContext.Projects.Where(p => categories.Any(c => c.Equals(p.CategoryId))).ToListAsync();
        }
    }
}
