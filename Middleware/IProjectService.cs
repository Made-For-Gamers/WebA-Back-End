using Datalayer.Models;

namespace Middleware
{
    public interface IProjectService
    {
        Task<IEnumerable<Project>> GetProjects(IEnumerable<Predicate<string>> filters, int skipElements, int elementsToTake);
    }
}